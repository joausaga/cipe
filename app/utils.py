import csv
import googlemaps
import logging
import urllib.request
import json
from django.conf import settings


gmaps = googlemaps.Client(key=f"{settings.GOOGLE_MAPS_API_KEY}")
logger = logging.getLogger(__name__)


def load_countries_iso2():
    iso_data = {}
    with open('data/iso3166-1.csv', 'r', encoding='utf-8-sig') as f:
        iso_file = csv.DictReader(f)
        for line in iso_file:
            iso_data[line['nombre'].lower()] = line['iso2'].lower()
    return iso_data


def get_location_info_from_coordinates_gmaps(latitude, longitude, language='es'):
    address, postal_code, city, region, country = '', '', '', '', ''
    logger.info(f"Going to look for information about the location with latitude {latitude} and "
                f"longitude {longitude}")
    try:
        reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude), language=language)
        for result in reverse_geocode_result:
            if result['types'][0] == 'route':
                address = result['formatted_address']
            if result['types'][0] == 'country':
                country = result['address_components'][0]['long_name']
            if result['types'][0] == 'administrative_area_level_1':
                region = result['address_components'][0]['long_name']
            if result['types'][0] == 'administrative_area_level_2':
                city = result['address_components'][0]['long_name']
            if result['types'][0] == 'postal_code':
                postal_code = result['address_components'][0]['long_name']
        logger.info(f"Information about the location was collected correctly!")
        return True, address, postal_code, city, region, country
    except Exception as e:
        logger.error(f"Error when doing reverse geo-coding {e}")
        return False, address, postal_code, city, region, country

def get_location_info_from_coordinates(latitude, longitude, language='es'):
    address, postal_code, city, region, country = '', '', '', '', ''
    logger.info(f"Going to look for information about the location with latitude {latitude} and "
                f"longitude {longitude}")          
    try:
        content = urllib.request.urlopen("https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=" + str(latitude) + "&lon="+str(longitude)).read() #consulto esta api de OSM 
        jsonResult=json.loads(content.decode(), parse_float=float)
        address = jsonResult['address']['road']
        postal_code = jsonResult['address']['postcode']
        city = jsonResult['address']['city']
        try:
            region = jsonResult['address']['state']
        except:
            try:
                region = jsonResult['address']['region']
            except:
                region=""
        country = jsonResult['address']['country']
        return True, address, postal_code, city, region, country
    except Exception as e:
        logger.error(f"Error when doing reverse geo-coding {e}")
        return False, address, postal_code, city, region, country


def get_location_info_from_name_gmaps(location_name, language='es'):
    address, postal_code, city, region, country = '', '', '', '', ''
    latitude, longitude = 0.0, 0.0
    logger.info(f"Going to look for information of location {location_name}")
    try:
        geocode_result = gmaps.geocode(location_name, language=language)
        for result in geocode_result[0]['address_components']:
            if result['types'][0] == 'postal_code':
                postal_code = result['long_name']
            if result['types'][0] == 'country':
                country = result['long_name']
            if result['types'][0] == 'administrative_area_level_1':
                region = result['long_name']
            if result['types'][0] == 'locality' or result['types'][0] == 'postal_town':
                city = result['long_name']
        if not city:
            city = region
        address = geocode_result[0]['formatted_address']
        coordinates = geocode_result[0]['geometry']['location']
        latitude, longitude = coordinates['lat'], coordinates['lng']
        logger.info(f"Information about the location was collected correctly!")
        return True, address, postal_code, city, region, country, latitude, longitude
    except Exception as e:
        logger.error(f"Error when doing geo-coding {e}")
        return False, address, postal_code, city, region, country, latitude, longitude

def get_location_info_from_name(location_name, language='es'):
    address, postal_code, city, region, country = '', '', '', '', ''
    latitude, longitude = 0.0, 0.0
    logger.info(f"Going to look for information of location {location_name}")
    queryFormat=locationName.replace(' ','+')   
    try:
        content = urllib.request.urlopen("https://nominatim.openstreetmap.org/search.php?q="+ queryFormat +"&format=json&limit=1&addressdetails=[1]").read() #consulto esta api de OSM 
        jsonResult=json.loads(content)
        ''' print(jsonResult[0]['address'])'''
        address = jsonResult[0]['address']['road']
        postal_code = jsonResult[0]['address']['postcode']
        city = jsonResult[0]['address']['city']
        try:
            region = jsonResult[0]['address']['state']
        except:
            try:
                region = jsonResult[0]['address']['region']
            except:
                region=""
        country = jsonResult[0]['address']['country']
        latitude = jsonResult[0]['lat']
        longitude = jsonResult[0]['lon']
        return True, address, postal_code, city, region, country, latitude, longitude
    except Exception as e:
        logger.error(f"Error when doing geo-coding {e}")
        return False, address, postal_code, city, region, country, latitude, longitude