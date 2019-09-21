import googlemaps
import logging

from app.forms import RegistrationForm
from app.models import Institution, Scientist, Affiliation
from django.shortcuts import render
from django.conf import settings


gmaps = googlemaps.Client(key=f"{settings.GOOGLE_MAPS_API_KEY}")
logger = logging.getLogger(__name__)


def __get_data_map():
    scientist_objs = Scientist.objects.all()
    scientists = []
    for scientist_obj in scientist_objs:
        scientist_institution = Affiliation.objects.select_related().get(scientist=scientist_obj).institution
        scientists.append(
            {'name': str(scientist_obj),
             'institution_name': scientist_institution.name,
             'institution_latitude': scientist_institution.latitude,
             'institution_longitude': scientist_institution.longitude
             },
        )
    num_scientists = len(scientists)
    num_institutions = Institution.objects.all().count()
    num_countries = Institution.objects.all().values('country').distinct().count()
    return scientists, num_scientists, num_institutions, num_countries


def index(request, *args, **kwargs):
    scientists, num_scientists, num_institutions, num_countries = __get_data_map()
    context = {
        'scientists': scientists,
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
        if form.is_valid():
            print(form.cleaned_data)
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
            scientist_obj, created = Scientist.objects.get_or_create(email=form.cleaned_data['email'],
                                                                     defaults=form.cleaned_data)
            if created:
                logger.info(f"Scientist {scientist_obj} created!")
                msg = f"El registro se completó exitosamente! Luego de su aprobación el mismo podrá ser visualizado en " \
                      f"el map del sitio."
            else:
                msg = f"El registro no se pudo completar debido a que email {form.cleaned_data['email']} ya se " \
                      f"encuentra registrado"
            affiliation_obj, created = Affiliation.objects.get_or_create(scientist=scientist_obj,
                                                                         institution=inst_obj,
                                                                         defaults={'scientist':scientist_obj,
                                                                                   'institution': inst_obj})
            form = RegistrationForm()
            registration_error = 0
        else:
            msg = f"Datos inválidos, favor compruebe los errores"
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
    context = {
        'scientists': scientists,
    }
    return render(request, 'map.html', context)