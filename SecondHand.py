import pickle
import time
import os
import json
from urllib.request import urlopen
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.geocoders import Nominatim
from geopy.distance import geodesic as GD
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
global listOfAllShops
listOfAllShops = []

def LoadPickleOut():
    try:
        with open('shopsData.pkl', 'rb') as shopsData:
            listOfAllShops = pickle.load(shopsData)
    except:
        print("You have 0 shops in Your database")

def UploadDataOut():
    with open('shopsData.pkl', 'wb') as shopsData:
        pickle.dump(listOfAllShops, shopsData)

def CheckInputInt():
    while True:
        try:
            choice = int(input())
            return choice
        except:
            print("Wrong input. Try again:")

def CheckInputFloat():
    while True:
        try:
            choice = float(input())
            return choice
        except:
            print("Wrong input. Try again:")

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

def Main():
    listOfAllShops = LoadPickleOut()
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

def GetYourLocationIP():
    latLongData = []
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
    while True:
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
                YourLocation = YourAddress(latitude, longitude, country, region, data['city'], data['suburb'], data['road'], None, location)
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
                try:
                    district = data['suburb']
                except:
                    district = None
                YourLocation = YourAddress(location.latitude, location.longitude, country, state, city, district, street, building, location)
                return YourLocation

def Menu(YourLocation):
    while True:
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
            case 2:
                YourShop = AddShopsManual(YourLocation)
                if not YourShop:
                    pass
                else:
                    YourShop.AddShopsSalesData()
            case 3:
                exit()

def AddShopsManual(YourLocation):
    geolocator = Nominatim(user_agent="MyApp")
    country = YourLocation.address['country']
    addressList = []
    addressList.append(country)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("///////////type 'exit' to return////////////")
        print("Enetr the name of the shop (it doesn't need to be real - what matters is that You will recognise it later)")
        name = input()
        if name == 'exit':
            YourShop = False
            return YourShop
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
                YourShop = False
                return YourShop
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
                YourShop = False
                return YourShop
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
                YourShop = False
                return YourShop
        addressList.append(building)
        address = ", ".join(addressList)
        location = geolocator.geocode(address, addressdetails=True)
        data = location.raw
        data = data['address']
        state = data['state']
        YourShop = SecondHandShop(location.latitude, location.longitude, name, country, state, city, street, building, location)
        UploadDataOut()
        return YourShop

def DisplayMyDatabase(YourLocation):
    for id in range(len(listOfAllShops)):
        distance = GD((str(YourLocation.latitude),str(YourLocation.longitude)), (listOfAllShops[id].latitude, listOfAllShops[id].longitude)).km
        print("({}) {} - {} - {} km from You".format(id, listOfAllShops[id].name, listOfAllShops[id].district, ))

class YourAddress:
    def __init__(self, latitude, longitude, country, region, city, district, street, building, location):
        self.latitude = latitude
        self.longitude = longitude
        self.address = {"country":country, "region":region, "city":city, "street":street,"district":district, "building":building, "location":location}
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
            radius = CheckInputFloat()
            if radius == 0:
                break            
            self.findShopsKM(radius)
    def findShopsKM(self, radius):
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
        self.getDistanceKM(radius) 
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
    def getDistanceKM(self, radius):
        os.system('cls' if os.name == 'nt' else 'clear')
        for loc in self.locations:
            self.distance.append(GD((str(loc.latitude),str(loc.longitude)), (self.latitude,self.longitude)).km)
        for id in range(len(self.locations)):
            if self.distance[id] <= radius and not (self.locations[id] in self.closestLocations):
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
        while True:
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
                    print("(1) Search my database")
                    print("(2) Return")
                    choice = CheckInputInt()
                    match choice:
                        case 0:
                            AddShopsManual(self)
                        case 1:
                            DisplayMyDatabase(self)


class SecondHandShop:
    def __init__(self, latitude, longitude, name, country, state, city, street, building, location):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.address = {"country":country, "region":state, "city":city, "street":street, "building":building, "location":location}
        self.prizes = {}
        listOfAllShops.append(self)
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
                    self.AddPrizes()
                case 1:
                    self.AddDeliveryDay()
                case 2:
                    break
        UploadDataOut()
    def AddDeliveryDay(self):
        while True:
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
                    break
            self.prizes['delivery day'] = delivery   
    def AddPrizes(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("(0) Add prizes according to the day of the week")
            print("(1) Add a note - prizes are different for each item")
            print("(2) Return")
            choice = CheckInputInt()
            os.system('cls' if os.name == 'nt' else 'clear')
            match choice:
                case 0:
                    print("Choose the day of the week:")
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
                            print("Enter the prize per kg on Monday or (0) return")
                            monday = input()
                            if monday == "0":
                                break
                            self.prizes['Monday'] = monday
                        case 1:
                            print("Enter the prize per kg on Tuesday or (0) return")
                            tuesday = input()
                            if tuesday == "0":
                                break
                            self.prizes['Tuesday'] = tuesday
                        case 2:
                            print("Enter the prize per kg on Wednesday or (0) return")
                            wednesday = input()
                            if wednesday == "0":
                                break
                            self.prizes['Wednesday'] = wednesday
                        case 3:
                            print("Enter the prize per kg on Thursday or (0) return")
                            thursday = input()
                            if thursday == "0":
                                break
                            self.prizes['Thursday'] = thursday
                        case 4:
                            print("Enter the prize per kg on Friday or (0) return")
                            friday = input()
                            if friday == "0":
                                break
                            self.prizes['Friday'] = friday
                        case 5:
                            print("Enter the prize per kg on Saturday or (0) return")
                            saturday = input()
                            if saturday == "0":
                                break
                            self.prizes['Saturday'] = saturday
                        case 6:
                            print("Enter the prize per kg on Sunday or (0) return")
                            sunday = input()
                            if sunday == "0":
                                break
                            self.prizes['Sunday'] = sunday
                        case 7:
                            print("bruh")
                            break
                case 1:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.prizes = {'Monday': "unspecified",'Tuesday': "unspecified", 'Wednesday': "unspecified", 'Thursday': "unspecified", 'Firday': "unspecified", 
                                   'Saturday': "unspecified", 'Sunday': "unspecified"}
                    print("Note added")
                    time.sleep(2)
                case 2:
                    break

Main()        

        