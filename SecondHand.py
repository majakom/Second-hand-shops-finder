import pickle
import os
import json
from urllib.request import urlopen
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.geocoders import Nominatim

def Main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("How would You like to get Your address?")
        print("(0) By entering Your location")
        print("(1) Via Your IP address (less accurate)")
        print("(2) Exit")
        choice = CheckInputInt()
        match choice:
            case 0:
                pass
            case 1:
                YourLocation = GetYourLocationIP()
            case 2:
                exit()


def CheckInputInt():
    while True:
        try:
            choice = int(input())
            break
        except:
            print("Wrong input. Try again:")
    return choice

def CheckInputFloat():
    while True:
        try:
            choice = float(input())
            break
        except:
            print("Wrong input. Try again:")
    return choice

def GetYourLocationIP():
    latLongData = []
    while True:
        urlopen("http://ipinfo.io/json")
        data = json.load(urlopen("http://ipinfo.io/json"))

        ip = data['ip']
        result = DbIpCity.get(ip, api_key="free")
        latitude = result.latitude
        longitude = result.longitude
        country = result.country
        region = result.region
        city = result.city
        latLongData.append(str(latitude))
        latLongData.append(str(longitude))
        geolocator = Nominatim(user_agent="GetLoc")
        location = geolocator.reverse(", ".join(latLongData))

        if city == None or region == None:
            print("Unfortunatelly there is no access to your location via Your IP address.")
            break

        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*len(str(location)))
        print(location)
        print("="*len(str(location))+"\n")
        print("Is this location meeting Your requirements?")
        print("(0) Yes")
        print("(1) No")
        choice = CheckInputInt()
        match choice:
            case 0:
                data = location.raw
                data = data['address']
                city = data['city']
                district = data['suburb']
                street = data['road']
                YourLocation = YourAddress(latitude, longitude)
                YourLocation.address["country"] = country
                YourLocation.address["region"] = region
                YourLocation.address["city"] = city
                YourLocation.address["district"] = district
                YourLocation.address["street"] = street
                YourLocation.address["building"] = None
                YourLocation.address["location"]= location
                return YourLocation
            case 1:
                break
            
class YourAddress:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.address = {}

        
Main()        

        