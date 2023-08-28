from geopy.geocoders import Nominatim
from ip2geotools.databases.noncommercial import DbIpCity
import json
from urllib.request import urlopen
import os
import math
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
                YourLocation.AreaChoice()
            case 1:
                YourLocation = EnterLocation()
                YourLocation.AreaChoice()
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
        ip = data['ip']
        res = DbIpCity.get(ip, api_key="free")
        latitude = res.latitude
        longitude = res.longitude
        city = res.city
        region = res.region
        country = res.country
        geolocator = Nominatim(user_agent="GetLoc")
        location = geolocator.reverse(str(latitude)+","+str(longitude))
        length = len(str(location))
        os.system('cls' if os.name == 'nt' else 'clear')
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
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Would You like to enter your location?")
                print("(0) No - exit")
                print("(1) Yes")
                choice = CheckInput()
                match choice:
                    case 0:
                        exit()
                    case 1:
                        YourLocation = EnterLocation()
                        YourLocation.AreaChoice()
            case 1:
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
            prGreen("(1) Skip and continue")
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
                            address = ", ".join(country, city, street)
                        case 1:
                            print("Enter the number of the building:")
                            building = input()
                            address = ", ".join(country, city, street, building)
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
                        address = ", ".join(country, city, district, street, building)
                        print(address)
                    else:
                        address = ", ".join(country, city, district, street)
                except:
                    YourLocation.address["district"] = None
                    os.system('cls' if os.name == 'nt' else 'clear')
                    if building != None:
                        address = ", ".join(country, city, street, building)
                        print(address)
                    else:
                        address = ", ".join(country, city, street)
                return YourLocation
            case "exit":
                exit()
            
class Location:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        self.address = {}
        self.chosenArea = []
    def AreaChoice(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=======Choose Your area======")
            print("(0) Enter the maximum distance from You")
            print("(1) Return")
            choice = CheckInput()
            match choice:
                case 0:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.AreaKM()
                case 1:
                    break
    def AreaKM(self):
        while True:
            print("(0) Return")
            print("Enter the number of the km:")
            nrKM = CheckInput()
            if nrKM == 0:
                break            
            ratioLat = 1/110.74
            ratioLong = (1/111.32)*math.acos(ratioLat)
            distanceNrLat = nrKM*ratioLat
            distanceNrLong = nrKM*ratioLong
            self.chosenArea.append(distanceNrLat)
            self.chosenArea.append(distanceNrLong)
            self.Shops()
    def Shops(self):
        geolocator = Nominatim(user_agent="name")
        address1 = ", ".join(["second hand", self.address["city"]])
        address2 = ", ".join(["używana odzież", self.address["city"]])
        address3 = ", ".join(["lumpeks", self.address["city"]])
        address4 = ", ".join(["sklep odzież", self.address["city"]])
        address5 = ", ".join(["sklep z ubraniami używanymi", self.address["city"]])
        address6 = ", ".join(["lump", self.address["city"]])
        address7 = ", ".join(["sklep z odzieżą używaną", self.address["city"]])
        address8 = ", ".join(["sklep z odzieżą", "lumpeks", self.address["city"]])
        address9 = ", ".join(["sklep odzieżowy", "używana", self.address["city"]])
        address10 = ", ".join(["lumpex", self.address["city"]])
        address11 = ", ".join(["używana", self.address["city"]])
        address12 = ", ".join(["vintage", "używana", self.address["city"]])
        address13 = ", ".join(["sklep", "odzież", "używana", self.address["city"]])
        address14 = ", ".join(["sklep odzieżowy", "lumpeks", self.address["city"]])
        address15 = ", ".join(["second hand shop", self.address["city"]])
        
        location1 = geolocator.geocode(address1, exactly_one =False)
        location2 = geolocator.geocode(address2, exactly_one =False)
        location3 = geolocator.geocode(address3, exactly_one =False)
        location4 = geolocator.geocode(address4, exactly_one =False)
        location5 = geolocator.geocode(address5, exactly_one =False)
        location6 = geolocator.geocode(address6, exactly_one =False)
        location7 = geolocator.geocode(address7, exactly_one =False)
        location8 = geolocator.geocode(address8, exactly_one =False)
        location9 = geolocator.geocode(address9, exactly_one =False)
        location10 = geolocator.geocode(address10, exactly_one =False)
        location11 = geolocator.geocode(address11, exactly_one =False)
        location12 = geolocator.geocode(address12, exactly_one =False)
        location13 = geolocator.geocode(address13, exactly_one =False)
        location14 = geolocator.geocode(address14, exactly_one =False)
        location15 = geolocator.geocode(address15, exactly_one =False)
        try:
            for loc in location1:
                print(loc.address)
        except:
            pass
        try:
            for loc in location2:
                print(loc.address)
        except:
            pass
        try:
            for loc in location3:
                print(loc.address)
        except:
            pass
        try:
            for loc in location4:
                print(loc.address)
        except:
            pass
        try:
            for loc in location5:
                print(loc.address)
        except:
            pass
        try:
            for loc in location6:
                print(loc.address)
        except:
            pass
        try:
            for loc in location7:
                print(loc.address)
        except:
            pass
        try:
            for loc in location8:
                print(loc.address)
        except:
            pass
        try:
            for loc in location9:
                print(loc.address)
        except:
            pass
        try:
            for loc in location10:
                print(loc.address)
        except:
            pass
        try:
            for loc in location11:
                print(loc.address)
        except:
            pass
        try:
            for loc in location12:
                print(loc.address)
        except:
            pass
        try:
            for loc in location13:
                print(loc.address)
        except:
            pass
        try:
            for loc in location14:
                print(loc.address)
        except:
            pass
        try:
            for loc in location15:
                print(loc.address)
        except:
            pass
        input()

Main()