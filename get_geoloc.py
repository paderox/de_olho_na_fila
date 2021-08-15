import myGoogleAPI
import urllib.request, urllib.parse, urllib.error
import ssl
import json

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def geocoding(address):
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"
    api_key = myGoogleAPI.googleAPI()
    parms = dict()
    parms["address"] = address
    parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    geocoding = json.loads(data)
    return geocoding
