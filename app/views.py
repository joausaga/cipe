import googlemaps
import logging
import json

from app.constants import SCIENTIFIC_AREA, POSITION
from app.forms import RegistrationForm
from app.models import Institution, Scientist, Affiliation
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse


gmaps = googlemaps.Client(key=f"{settings.GOOGLE_MAPS_API_KEY}")
logger = logging.getLogger(__name__)


def __get_data_map(scientific_area='', position='', becal=False):
    query = {'has_becal_scholarship': becal, 'approved': True}
    if scientific_area != '':
        query['scientific_area'] = scientific_area
    if position != '':
        query['position'] = position
    scientist_objs = Scientist.objects.filter(**query)
    scientists = []
    institutions = []
    countries = []
    for scientist_obj in scientist_objs:
        scientist_institution = Affiliation.objects.select_related().get(scientist=scientist_obj, current=True).institution
        scientists.append(
            {'name': str(scientist_obj),
             'scientific_area': scientist_obj.get_scientific_area_display(),
             'position':  scientist_obj.get_position_display(),
             'twitter_handler': scientist_obj.twitter_handler,
             'facebook_profile': scientist_obj.facebook_profile,
             'gscholar_profile': scientist_obj.gscholar_profile,
             'scopus_profile': scientist_obj.scopus_profile,
             'linkedin_profile': scientist_obj.linkedin_profile,
             'researchgate_profile': scientist_obj.researchgate_profile,
             'academia_profile': scientist_obj.academia_profile,
             'institutional_website': scientist_obj.institutional_website,
             'personal_website': scientist_obj.personal_website,
             'orcid_profile': scientist_obj.orcid_profile,
             'becal_fellow': scientist_obj.has_becal_scholarship,
             'institution_name': scientist_institution.name,
             'institution_latitude': scientist_institution.latitude,
             'institution_longitude': scientist_institution.longitude,
             'institution_country': scientist_institution.country,
             'institution_city': scientist_institution.city,
             },
        )
        institutions.append(scientist_institution.name)
        countries.append(scientist_institution.country)
    num_scientists = len(scientists)
    num_institutions = len(set(institutions))
    num_countries = len(set(countries))
    return scientists, num_scientists, num_institutions, num_countries


def index(request, *args, **kwargs):
    scientists, num_scientists, num_institutions, num_countries = __get_data_map()
    context = {
        'scientists': json.dumps(scientists),
        'num_scientists': num_scientists,
        'num_institutions': num_institutions,
        'num_countries': num_countries,
        'message': kwargs['msg'] if 'msg' in kwargs else ''
    }
    return render(request, 'index.html', context)


def __get_institution_extra_information(inst_dict):
    try:
        reverse_geocode_result = gmaps.reverse_geocode((inst_dict['latitude'], inst_dict['longitude']))
        inst_dict['address'] = reverse_geocode_result[0]['formatted_address']
        inst_dict['city'] = reverse_geocode_result[0]['address_components'][3]['long_name']
        inst_dict['region'] = reverse_geocode_result[0]['address_components'][4]['long_name']
        inst_dict['country'] = reverse_geocode_result[0]['address_components'][5]['long_name']
        inst_dict['postal_code'] = reverse_geocode_result[0]['address_components'][6]['long_name']
        return True, inst_dict
    except Exception as e:
        logger.error(f"Error when doing reverse geo-coding {e}")
        return False, inst_dict


def registration(request):
    msg = ''
    registration_error = -1
    created = False
    form = RegistrationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid() and form.cleaned_data['location_lat'] != '' and form.cleaned_data['location_lng'] != '' and \
           form.cleaned_data['location_name'] != '':
            try:
                Scientist.objects.get(email=form.cleaned_data['email'], ci=form.cleaned_data['ci'])
                msg = f"Investigador con email {form.cleaned_data['email']} y cédula de identidad " \
                      f"{form.cleaned_data['ci']} ya existente"
                registration_error = 1
            except Scientist.DoesNotExist:
                # Get institution data
                inst_dict = {
                    'latitude': form.cleaned_data['location_lat'],
                    'longitude': form.cleaned_data['location_lng'],
                    'name': form.cleaned_data['location_name']
                }
                # Get institution country and city
                try:
                    inst_obj = Institution.objects.get(latitude=inst_dict['latitude'], longitude=inst_dict['longitude'])
                    if inst_obj.country == '':
                        success, inst_dict = __get_institution_extra_information(inst_dict)
                        if success:
                            inst_obj, updated = Institution.objects.update_or_create(latitude=inst_dict['latitude'],
                                                                                    longitude=inst_dict['longitude'],
                                                                                    defaults=inst_dict)
                except Institution.DoesNotExist:
                    _, inst_dict = __get_institution_extra_information(inst_dict)
                    inst_obj = Institution(**inst_dict)
                    inst_obj.save()
                    logger.info(f"Institution {inst_dict} created!")
                # Remove institution data from form object
                del form.cleaned_data['location_lat']
                del form.cleaned_data['location_lng']
                del form.cleaned_data['location_name']
                # Get/Create Scientist
                scientist_obj = Scientist.objects.create(**form.cleaned_data)
                scientist_obj.save()
                logger.info(f"Scientist {scientist_obj} created!")
                affiliation_obj, created = Affiliation.objects.get_or_create(scientist=scientist_obj,
                                                                             institution=inst_obj,
                                                                             defaults={'scientist': scientist_obj,
                                                                                       'institution': inst_obj})
                msg = f"Registro exitoso!\nLuego de su aprobación los datos del mismo podrá ser " \
                      f"visualizado en el map de investigadores."
                form = RegistrationForm()
                registration_error = 0
        else:
            if form.cleaned_data['location_name'] == '' or form.cleaned_data['location_lat'] == '' or \
               form.cleaned_data['location_lng'] == '':
                msg = f"Datos de registro incompletos, favor indique una institución"
                logger.info(f"Registration Error: Missing institution. Form details {form}")
            else:
                msg = "Datos inválidos, favor compruebe los errores"
                logger.info(f"Registration Error: The form is not valid. Form details {form}")
            registration_error = 1
    context = {
        'form': form,
        'msg': msg,
        'registration_result': registration_error
    }
    if created:
        logger.info(f"Affiliation {affiliation_obj} created!")
        return render(request, 'register.html', context)
    else:
        return render(request, 'register.html', context)


def success_registration(request):
    return render(request, 'success.html')


def map_scientists(request):
    scientists, _, _, _ = __get_data_map()
    value_scientific_areas = []
    value_positions = []
    exists_becal_scholar = False
    for scientist in scientists:
        if scientist['scientific_area'] not in value_scientific_areas:
            value_scientific_areas.append(scientist['scientific_area'])
        if scientist['position'] not in value_positions:
            value_positions.append(scientist['position'])
        if not exists_becal_scholar and scientist['becal_fellow']:
            exists_becal_scholar = True
    scientific_areas = []
    for value_scientific_area in value_scientific_areas:
        for scientific_area in SCIENTIFIC_AREA:
            if scientific_area[1] == value_scientific_area:
                scientific_areas.append(scientific_area)
                break
    positions = []
    for value_position in value_positions:
        for position in POSITION:
            if position[1] == value_position:
                positions.append(position)
    context = {
        'scientists': json.dumps(scientists),
        'scientific_areas': scientific_areas,
        'positions': positions,
        'exists_becal_scholar': exists_becal_scholar
    }
    return render(request, 'map.html', context)


def filter_map(request):
    if request.method == 'POST':
        position = request.POST.get('position')
        scientific_area = request.POST.get('scientific_area')
        becal = request.POST.get('becal')
        scientists, _, _, _ = __get_data_map(scientific_area, position, becal == 'true')
        response_data = {
            'scientists': scientists,
        }
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"msg": "Cannot recognize the method type"}),
            content_type="application/json"
        )