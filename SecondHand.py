import pickle
import os
import json
from urllib.request import urlopen
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.geocoders import Nominatim
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

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
                YourLocation = EnterYourLocation()
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

def EnterYourLocation():
    street = None
    building = None
    country = "Poland"
    addressList = []
    addressList.append(country)
    geolocator = Nominatim(user_agent="MyApp")
    
    while True:
        if street == None and building == None:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Enter the name of the city or (0) return")
            city = input()
            if city == "0":
                break
            addressList.append(city)

        os.system('cls' if os.name == 'nt' else 'clear')
        print("=========Choose optionally:=========")
        if street == None or street == "0":
            print("(0) Enter the name of the street")
        else:
            prRed("(0) Enter the name of the street")
        if building == None or building == "0":
            print("(1) Enter the number of the building")
        else:
            prRed("(1) Enter the number of the building")
        if (building != None and building != "0") or (street != None and street != "0"):
            prGreen("(2) Skip and/or continue")
        choice = CheckInputInt()
        os.system('cls' if os.name == 'nt' else 'clear')
        match choice:
            case 0:
                print("Enter the name of the street or (0) return:")
                street = input()
                if street == "0":
                    pass
                else:
                    addressList.append(street)
            case 1:
                print("Enter the number of the building or (0) return")
                building = input()
                if building == "0":
                    pass
                else:
                    addressList.append(building)
            case 2:
                address = ", ".join(addressList)
                location = geolocator.geocode(address, addressdetails=True)
                data = location.raw
                data = data['address']
                state = data['state']
                YourLocation = YourAddress(location.latitude, location.longitude)
                YourLocation.address["country"] = country
                YourLocation.address["region"] = state
                YourLocation.address["city"] = city
                YourLocation.address["street"] = street
                YourLocation.address["building"] = building
                YourLocation.address["location"]= location
                try:
                    district = data['suburb']
                    print(district)
                    YourLocation.address["district"] = district
                    input()
                except:
                    YourLocation.address["district"] = None
                return YourLocation

class YourAddress:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.address = {}

        
Main()        

        