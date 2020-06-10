import csv
import googlemaps
import logging
import urllib.request
import json
from django.conf import settings
from urllib.parse import urlencode

gmaps = googlemaps.Client(key=f"{settings.GOOGLE_MAPS_API_KEY}")
logger = logging.getLogger(__name__)


def load_countries_iso2():
    iso_data = {}
    with open('data/iso3166-1.csv', 'r', encoding='utf-8-sig') as f:
        iso_file = csv.DictReader(f)
        for line in iso_file:
            iso_data[line['nombre'].lower()] = line['iso2'].lower()
    return iso_data

def get_location_info_from_coordinates(latitude, longitude, language='es'):
    address, postal_code, city, region, country = '', '', '', '', ''
    logger.info(f"Going to look for information about the location with latitude {latitude} and "
                f"longitude {longitude}")
    mydict = {'format': 'jsonv2', 'lat': str(latitude), 'lon': str(longitude)}
    urlencode(mydict)
    query = urlencode(mydict)
    try:
        #look up OSM's API
        content = urllib.request.urlopen("https://nominatim.openstreetmap.org/reverse?"+query).read() 
        json_result=json.loads(content.decode(), parse_float=float)
        if 'address' in json_result:
            if 'road' in json_result['address']:
                address = json_result['address']['road']
            if 'postcode' in json_result['address']:
                postal_code = json_result['address']['postcode']
            if 'city' in json_result['address']:
                city = json_result['address']['city']
            if 'state' in json_result['address']:
                region = json_result['address']['state']
            elif 'region' in json_result['address']:
                region = json_result['address']['region']
            if 'country' in json_result['address']:
                country = json_result['address']['country']
        return True, address, postal_code, city, region, country
    except Exception as e:
        logger.error(f"Error when doing reverse geo-coding {e}")
        return False, address, postal_code, city, region, country

def get_location_info_from_name(location_name, language='es'):
    address, postal_code, city, region, country = '', '', '', '', ''
    latitude, longitude = 0.0, 0.0
    logger.info(f"Going to look for information of location {location_name}")
    mydict = {'q': locationName, 'format': 'json', 'limit': '1', 'addressdetails': '[1]'}
    urlencode(mydict)
    query = urlencode(mydict)
    try:
        #look up OSM's API
        content = urllib.request.urlopen("https://nominatim.openstreetmap.org/search.php?"+query).read()
        json_result=json.loads(content)
        if 'address' in json_result[0]:
            if 'road' in json_result[0]['address']:
                address = json_result[0]['address']['road']
            if 'postcode' in json_result[0]['address']:
                postal_code = json_result[0]['address']['postcode']
            if 'city' in json_result[0]['address']:
                city = json_result[0]['address']['city']
            if 'state' in json_result[0]['address']:
                region = json_result[0]['address']['state']
            elif 'region' in json_result[0]['address']:
                region = json_result[0]['address']['region']
            if 'country' in json_result[0]['address']:
                country = json_result[0]['address']['country']
        if 'lat' in json_result[0]:
            latitude = json_result[0]['lat']
        if 'lon' in json_result[0]:
            longitude = json_result[0]['lon']
        return True, address, postal_code, city, region, country, latitude, longitude
    except Exception as e:
        logger.error(f"Error when doing geo-coding {e}")
        return False, address, postal_code, city, region, country, latitude, longitude