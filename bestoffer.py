from geopy.geocoders import Nominatim
from ip2geotools.databases.noncommercial import DbIpCity
import json
from urllib.request import urlopen
import os

def Main():
    while True:
        print("How would You like to get your closest area?")
        print("(0) Via IP address")
        print("(1) Enter your location (more accurate)")
        choice = CheckInput()
        match choice:
            case 0:
                YourLocation = GetLocationIP()
            case 1:
                country = "Poland"
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Enter the name of the city:")
                city = input()
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Enter the name of the district/street")
                district = input()

def CheckInput():
    while True:
        try:
            choice = int(input())
            break
        except:
            print("Wrong input. Try again:")
    return choice

def GetLocationIP():
    while True:
        urlopen("http://ipinfo.io/json")
        data = json.load(urlopen("http://ipinfo.io/json"))
        ip = data['ip']
        res = DbIpCity.get(ip, api_key="free")
        latitude = res.latitude
        longitude = res.longitude
        city = res.city
        region = res.region
        country = res.country
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(str(latitude)+","+str(longitude))
        print(location)
        #print(region)
        #print(city)
        print(latitude)
        print(longitude)
        if city == None:
            print("Unfortunatelly there is no access to your location via your IP address.")
            break
        if region == None:
            print("Unfortunatelly there is no access to your location via your IP address.")
            break
        print("Is it close enough to You?")
        print("(0) No")
        print("(1) Yes")
        choice = CheckInput()
        match choice:
            case 0:
                print("Would You like to enter your location?")
                print("(0) No - exit")
                print("(1) Yes")
                choice = CheckInput()
                match choice:
                    case 0:
                        exit()
                    case 1:
                        YourLocation = EnterLocation()
            case 1:
                pass


        YourLocation = Location(country, city, region, None, None, latitude, longitude)
        return YourLocation
    

def EnterLocation():
    geolocator = Nominatim(user_agent="MyApp")
    country = "Poland"
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Enter the name of the city:")
    city = input()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Enter the name of the district and/or street and/or building number")
    district = input()
    address = country+", "+city+", "+district
    location = geolocator.geocode(address, addressdetails=True)
    print(location.raw)
    YourLocation = Location(country, city, region, None, None, location.latitude, location.longitude)
    return YourLocation
class Location:
    def __init__(self, country, city, region, street, building, lat, long,):
        self.country = country
        self.city = city
        self.region = region
        self.street = street
        self.building = building
        self.lat = lat
        self.long = long
        
    
#geolocator = Nominatim(user_agent="MyApp")
#address  = ""
#location = geolocator.geocode(address, addressdetails=True)
#print(location.raw)
#print()
#print(location.longitude)

Main()