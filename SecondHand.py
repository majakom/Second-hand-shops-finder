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
        Menu(YourLocation)

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

def Menu(YourLocation):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("========Choose:==========")
    print("(0) Find Shops in Your Area")
    print("(1) Select a shop from Your database")
    print("(2) Add a shop to Your database")
    print("(3) Exit")
    choice = CheckInputInt()
    match choice:
        case 0:
            YourLocation.AreaChoice()


class YourAddress:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.address = {}
        self.locations = []
    def AreaChoice(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("====================Choose:=====================")
            print("(0) Enter the maximum distance from shop to You")
            print("(1) Search via the district You are currently in")
            print("(2) Return")
            choice = CheckInputInt()
            os.system('cls' if os.name == 'nt' else 'clear')
            match choice:
                case 0:
                    self.AreaKM()
                case 1:
                    self.findShopsInDistrict()
                case 2:
                    break
    def AreaKM(self):
        while True:
            print("Enter the number of the km or (0) return:")
            self.radius = CheckInputFloat()
            if self.radius == 0:
                break            
            self.findShopsKM()
    def findShopsKM(self):
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
        address12 = ", ".join(["vintage", "sklep z odzieżą używaną", self.address["city"]])
        address13 = ", ".join(["sklep", "odzież", "używana", self.address["city"]])
        address14 = ", ".join(["sklep odzieżowy", "lumpeks", self.address["city"]])
        address15 = ", ".join(["second hand shop", self.address["city"]])
        address16 = ", ".join(["komis", "sklep z odzieżą używaną", self.address["city"]])
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
        location16 = geolocator.geocode(address16, exactly_one =False)
        try:
            for loc in location1:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location2:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location3:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location4:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location5:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location6:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location7:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location8:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location9:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location10:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location11:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location12:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location13:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location14:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location15:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location16:
                self.locations.append(loc)
        except:
            pass  
    def findShopsInDistrict(self):
        geolocator = Nominatim(user_agent="name")
        address1 = ", ".join(["second hand", self.address['district'], self.address["city"]])
        address2 = ", ".join(["używana odzież", self.address['district'], self.address["city"]])
        address3 = ", ".join(["lumpeks", self.address['district'], self.address["city"]])
        address4 = ", ".join(["sklep odzież", self.address['district'], self.address["city"]])
        address5 = ", ".join(["sklep z ubraniami używanymi", self.address['district'], self.address["city"]])
        address6 = ", ".join(["lump", self.address['district'], self.address["city"]])
        address7 = ", ".join(["sklep z odzieżą używaną", self.address['district'], self.address["city"]])
        address8 = ", ".join(["sklep z odzieżą", "lumpeks", self.address['district'], self.address["city"]])
        address9 = ", ".join(["sklep odzieżowy", "używana", self.address['district'], self.address["city"]])
        address10 = ", ".join(["lumpex", self.address['district'], self.address["city"]])
        address11 = ", ".join(["używana", self.address['district'], self.address["city"]])
        address12 = ", ".join(["vintage", "sklep z odzieżą używaną", self.address['district'], self.address["city"]])
        address13 = ", ".join(["sklep", "odzież", "używana", self.address['district'], self.address["city"]])
        address14 = ", ".join(["sklep odzieżowy", "lumpeks", self.address['district'], self.address["city"]])
        address15 = ", ".join(["second hand shop", self.address['district'], self.address["city"]])
        address16 = ", ".join(["komis", "sklep z odzieżą używaną", self.address["city"]])
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
        location16 = geolocator.geocode(address16, exactly_one =False)
        try:
            for loc in location1:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location2:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location3:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location4:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location5:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location6:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location7:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location8:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location9:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location10:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location11:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location12:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location13:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location14:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location15:
                self.locations.append(loc)
        except:
            pass
        try:
            for loc in location16:
                self.locations.append(loc)
        except:
            pass 
Main()        

        