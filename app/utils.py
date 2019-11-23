import googlemaps
import logging

from django.conf import settings


gmaps = googlemaps.Client(key=f"{settings.GOOGLE_MAPS_API_KEY}")
logger = logging.getLogger(__name__)


def get_location_info_from_coordinates(latitude, longitude, language='es'):
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


def get_location_info_from_name(location_name, language='es'):
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
            if result['types'][0] == 'administrative_area_level_2' or result['types'][0] == 'locality':
                city = result['long_name']
            if result['types'][0] == 'route':
                address = result['long_name']
        coordinates = geocode_result[0]['geometry']['location']
        latitude, longitude = coordinates['lat'], coordinates['lng']
        logger.info(f"Information about the location was collected correctly!")
        return True, address, postal_code, city, region, country, latitude, longitude
    except Exception as e:
        logger.error(f"Error when doing geo-coding {e}")
        return False, address, postal_code, city, region, country, latitude, longitude
