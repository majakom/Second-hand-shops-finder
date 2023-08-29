import pickle
import os
import json
from urllib.request import urlopen
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.geocoders import Nominatim
from geopy.distance import geodesic as GD
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

def CheckInputForExit():
    while True:
        try:
            choice = int(input())
            return choice
        except:
            choice = input()
            choice.lower()
            if choice == 'exit':
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
        case 1:
            YourShop = AddShopsManual(YourLocation)
            YourShop.AddShopsSalesData()

        case 3:
            exit()

def LoadPickleOut():
        listOfAllShops = []
        try:
            if os.path.isfile("shopsData.pkl"):
                with open('shopsData.pkl', 'rb') as shopsData:
                    listOfAllShops = pickle.load(shopsData)
                return listOfAllShops
        except:
            print("You have 0 shops in Your database")
            pass
def UploadDataOut(listOfAllShops):
    with open('shopsData.pkl', 'wb') as shopsData:
        pickle.dump(listOfAllShops, shopsData)
def AddShopsManual(YourLocation):
    geolocator = Nominatim(user_agent="MyApp")
    country = YourLocation.address['country']
    addressList = []
    addressList.append(country)
    while True:
        listOfAllShops = LoadPickleOut()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("///////////type 'exit' to return////////////")
        print("Is the new shop in the same city You are in?")
        print("(0) Yes")
        print("(1) No - enter the name of the city")
        choice = CheckInputForExit()
        match choice:
            case 0:
                city = YourLocation.address['city']
            case 1:
                city = input()
            case 'exit':
                break
        addressList.append(city)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("/////////////type 'exit' to return////////////")
        print("Is the new shop on the same street You are on?")
        print("(0) Yes")
        print("(1) No - enter the name of the street")
        choice = CheckInputForExit()
        match choice:
            case 0:
                street = YourLocation.address['street']
            case 1:
                street = input()
            case 'exit':
                break
        addressList.append(street)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("////////////type 'exit' to return///////////////")
        print("Is the new shop in the same building You are in?")
        print("(0) Yes")
        print("(1) No - enter the number of the building")
        choice = CheckInputForExit()
        os.system('cls' if os.name == 'nt' else 'clear')
        match choice:
            case 0:
                if YourLocation.address['building'] == None:
                    print("The number of the building is unknown")
                    print("Enter it now:")
                    building = input()
                else:
                    building = YourLocation.address['building']
            case 1:
                building = input()
            case 'exit':
                break
        addressList.append(building)
        address = ", ".join(addressList)
        location = geolocator.geocode(address, addressdetails=True)
        data = location.raw
        data = data['address']
        state = data['state']
        YourShop = SecondHandShop(location.latitude, location.longitude)
        YourShop.address["country"] = country
        YourShop.address["region"] = state
        YourShop.address["city"] = city
        YourShop.address["street"] = street
        YourShop.address["building"] = building
        YourShop.address["location"]= location
        return YourShop

                


class YourAddress:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.address = {}
        self.locations = []
        self.distance = []
        self.closestLocations = []
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
        self.getDistanceKM() 
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
        self.DistrictSearch() 
    def getDistanceKM(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for loc in self.locations:
            self.distance.append(GD((str(loc.latitude),str(loc.longitude)), (self.latitude,self.longitude)).km)
        for id in range(len(self.locations)):
            if self.distance[id] <= self.radius and not (self.locations[id] in self.closestLocations):
                self.closestLocations.append(self.locations[id])  
        for id in range(len(self.closestLocations)):
            print("({}) {} {} {}".format(id, self.closestLocations[id], str(self.closestLocations[id].latitude), str(self.closestLocations[id].longitude)))
        print("\n=====================================")
        print("(0) Choose a shop and check the details")
        print("(1) I didn't find my shop")
        choice = CheckInputInt()
        os.system('cls' if os.name == 'nt' else 'clear')
        match choice:
            case 0:
                for id in range(len(self.closestLocations)):
                    print("({}) {} {} {}".format(id, self.closestLocations[id], str(self.closestLocations[id].latitude), str(self.closestLocations[id].longitude)))
                print("\n=====================================")
                print("Enter the number of the shop:")
                choice = CheckInputInt()
            case 1:
                print("(0) Add a shop")
                print("(1) Return")
                choice = CheckInputInt()
    def DistrictSearch(self):
        self.locations = self.closestLocations
        for id in range(len(self.closestLocations)):
            print("({}) {}".format(id, self.closestLocations[id]))
        print("\n=====================================")
        print("(0) Choose a shop and check the details")
        print("(1) I didn't find my shop")
        choice = CheckInputInt()
        os.system('cls' if os.name == 'nt' else 'clear')
        match choice:
            case 0:
                for id in range(len(self.closestLocations)):
                    print("({}) {}".format(id, self.closestLocations[id]))
                print("\n=====================================")
                print("Enter the number of the shop:")
                choice = CheckInputInt()
            case 1:
                print("(0) Add a shop")
                print("(1) Return")
                choice = CheckInputInt()

class SecondHandShop:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.address = {}
        self.prizes = {}
    def AddShopsSalesData(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Add data:")
            print("(0) Add prizes")
            print("(1) Add delivery day")
            print("(2) Return")
            choice = CheckInputInt()
            match choice:
                case 0:
                    self.AddPrizes(self)
                case 1:
                    self.AddDeliveryDay(self)
                case 2:
                    break
    def AddDeliveryDay(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Choose the day of the delivery:")
        print("(0) Monday")
        print("(1) Tuesday")
        print("(2) Wednesday")
        print("(3) Thursday")
        print("(4) Friday")
        print("(5) Saturday")
        print("(6) Sunday")
        print("(7) Return")
        choice = CheckInputInt()
        match choice:
            case 0:
                delivery = "Monday"
            case 1:
                delivery = "Tuesday"
            case 2:
                delivery = "Wednesday"
            case 3:
                delivery = "Tuesday"
            case 4:
                delivery = "Friday"
            case 5:
                delivery = "Saturday"
            case 6:
                delivery = "Sunday"
            case 7:
                return
        self.prizes['delivery day'] = delivery   
    #def AddPrizes(self):



Main()        

        