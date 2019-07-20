import googlemaps

from app.forms import RegistrationForm
from app.models import Institution, Scientist, Affiliation
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings


gmaps = googlemaps.Client(key=f"{settings.GOOGLE_MAPS_API_KEY}")


def index(request):
    context = {
        'lat': 41.389633,
        'lon': 40.116217
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
    except:
        return False, inst_dict


def registration(request):
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
            # Remove institution data from form object
            del form.cleaned_data['location_lat']
            del form.cleaned_data['location_lng']
            del form.cleaned_data['location_name']
            # Get/Create Scientist
            scientist_obj, created = Scientist.objects.get_or_create(email=form.cleaned_data['email'],
                                                                     defaults=form.cleaned_data)
            if created:
                # log
                pass
            affiliation_obj, created = Affiliation.objects.get_or_create(scientist=scientist_obj,
                                                                         institution=inst_obj,
                                                                         defaults={'scientist':scientist_obj,
                                                                                   'institution': inst_obj})
            if created:
                # log
                pass
            return HttpResponseRedirect('/')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def success_registration(request):
    return render(request, 'success.html')


def map_scientists(request):
    context = {
        'lat': 41.389633,
        'lon': 2.116217
    }
    return render(request, 'map.html', context)