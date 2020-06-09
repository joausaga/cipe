import csv
import googlemaps
import logging
import urllib.request
import json
from django.conf import settings
from urllib.parse import urlencode

DICTIONARY= {}
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
    try:
        #look up OSM's API
        content = urllib.request.urlopen("https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=" + str(latitude) + "&lon="+str(longitude)).read() 
        json_result=json.loads(content.decode(), parse_float=float)
        address = json_result['address']['road']
        postal_code = json_result['address']['postcode']
        city = json_result['address']['city']
        try:
            region = json_result['address']['state']
        except:
            try:
                region = json_result['address']['region']
            except:
                region=""
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
        address = json_result[0]['address']['road']
        postal_code = json_result[0]['address']['postcode']
        city = json_result[0]['address']['city']
        try:
            region = json_result[0]['address']['state']
        except:
            try:
                region = json_result[0]['address']['region']
            except:
                region=""
        country = json_result[0]['address']['country']
        latitude = json_result[0]['lat']
        longitude = json_result[0]['lon']
        return True, address, postal_code, city, region, country, latitude, longitude
    except Exception as e:
        logger.error(f"Error when doing geo-coding {e}")
        return False, address, postal_code, city, region, country, latitude, longitude