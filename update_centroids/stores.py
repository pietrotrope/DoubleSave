import requests
from constants import salling_token

headers = {"Authorization": salling_token}

arguments = {'country': 'DK', "geo":"55.67,12.57", "radius":20, "per_page":1000}

req = requests.get("https://api.sallinggroup.com/v2/stores/", headers=headers, params=arguments)



with open("stores.json", "w") as outfile:
    outfile.write(req.text)