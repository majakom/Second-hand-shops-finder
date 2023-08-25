from geopy.geocoders import Nominatim
from ip2geotools.databases.noncommercial import DbIpCity
import json
from urllib.request import urlopen
import os
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))


def Main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("How would You like to get your closest area?")
        print("(0) Via IP address")
        print("(1) Enter your location (more accurate)")
        print("(2) Exit")
        choice = CheckInput()
        match choice:
            case 0:
                YourLocation = GetLocationIP()
            case 1:
                YourLocation = EnterLocation()
            case 2:
                exit()

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
        print(data)
        ip = data['ip']
        print(ip)
        res = DbIpCity.get(ip, api_key="free")
        latitude = res.latitude
        longitude = res.longitude
        city = res.city
        region = res.region
        country = res.country
        print(latitude)
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(str(latitude)+","+str(longitude))
        print(location)
        length = len(str(location))
        print('\n'+"="*length)
        print(location)
        print("="*length+"\n")
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
                #print(res.raw)
                cityData = city.split(sep = "(")
                cityData[1] = cityData[1].replace(")", "")
                YourLocation = Location(latitude, longitude)
                YourLocation.address["country"] = country
                YourLocation.address["region"] = region
                YourLocation.address["city"] = cityData[0]
                YourLocation.address["district"] = cityData[1]
                YourLocation.address["street"] = None
                YourLocation.address["building"] = None
                YourLocation.address["location"]= location
                return YourLocation
    

def EnterLocation():
    street = None
    building = None
    country = "Poland"
    geolocator = Nominatim(user_agent="MyApp")
    while True:
        if street != "0" and street == None:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Enter the name of the city:")
            city = input()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Enter:")
        if street != "0" and street != None:
            prRed("(0) the name of the street")
            prGreen("(1) Continue")
        else:    
            print("(0) the name of the street")
        choice = CheckInput()
        os.system('cls' if os.name == 'nt' else 'clear')
        match choice:
            case 0:
                print("(0) return")
                print("Enter the name of the street:")
                street = input()
                if street == "0":
                    pass
                else:
                    print("\n=================================================")
                    print("Would You like to add the number of the building?")
                    print("(0) No")
                    print("(1) Yes")
                    choice = CheckInput()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    match choice:
                        case 0:
                            building = None
                            address = country+", "+city+", "+street
                        case 1:
                            print("Enter the number of the building:")
                            building = input()
                            address = country+", "+city+", "+street+" "+building
                    pass
            case 1:
                location = geolocator.geocode(address, addressdetails=True)
                data = location.raw
                data = data['address']
                state = data['state']
                YourLocation = Location(location.latitude, location.longitude)
                YourLocation.address["country"] = country
                YourLocation.address["region"] = state
                YourLocation.address["city"] = city
                YourLocation.address["street"] = street
                YourLocation.address["building"] = building
                YourLocation.address["location"]= location
                try:
                    district = data['neighbourhood']
                    YourLocation.address["district"] = district
                    os.system('cls' if os.name == 'nt' else 'clear')
                    if building != None:
                        address = country+", "+city+", "+district+", "+street+" "+building
                        print(address)
                    else:
                        address = country+", "+city+", "+district+", "+street
                except:
                    YourLocation.address["district"] = None
                    os.system('cls' if os.name == 'nt' else 'clear')
                    if building != None:
                        address = country+", "+city+", "+street+" "+building
                        print(address)
                    else:
                        address = country+", "+city+", "+street
                input()
                return YourLocation
            case "exit":
                exit()
            
class Location:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        self.address = {}




    
#geolocator = Nominatim(user_agent="MyApp")
#address  = ""
#location = geolocator.geocode(address, addressdetails=True)
#print(location.raw)
#print()
#print(location.longitude)

Main()