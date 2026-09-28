import requests
from server.data.tools.constants import Google_geocoord_token

arguments = {'address': 'central station, København', "key":Google_geocoord_token}

req = requests.get("https://maps.googleapis.com/maps/api/geocode/json",params=arguments)


print(req.text)