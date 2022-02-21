import requests
import json

url = 'https://extreme-ip-lookup.com/json/'
r = requests.get(url)
data = json.loads(r.content.decode())
ip = data['query']
response = requests.get("https://geolocation-db.com/json/"+ip+"&position=true").json()
lat = response['latitude']
lon = response['longitude']
print("Latitude: ", lat)
print("Longitude: ", lon)