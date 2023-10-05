import pickle
import time
import os
import json
from urllib.request import urlopen
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.geocoders import Nominatim
from geopy.distance import geodesic as GD
geolocator = Nominatim(user_agent="GetLoc")
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

global listOfAllShops
listOfAllShops = []
global addressList
addressList = []
global latLongData
latLongData = []
global newLocations
newLocations = []
global addressShop
addressShop = []

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
        choice = input()
        if choice == 'exit':
            return choice
        try:
            if type(int(choice)) == int:
                return int(choice)
        except:
            print("Wrong input. Try again:")

def Main():
    LoadData()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=======================================")
        print("Get Your location:")
        print("(0) Via Your IP address (less accurate)")
        print("(1) By entering Your location")
        print("(2) Exit")
        print("=======================================")
        choice = CheckInputForExit()
        match choice:
            case 0:
                YourLocation = GetYourLocationIP()
            case 1:
                YourLocation = EnterYourLocation()
            case 2:
                exit()
            case 'exit':
                exit()
        if YourLocation:
            Menu(YourLocation)

def GetYourLocationIP():
    addressList.clear()
    try:
        urlopen("http://ipinfo.io/json")
        data = json.load(urlopen("http://ipinfo.io/json"))
    except:
        print("Sorry. Your internet connection is unstable right now. Try again later")
        time.sleep(2)
        return
    ip = data['ip']
    result = DbIpCity.get(ip, api_key="free")
    latitude = result.latitude
    longitude = result.longitude
    latLongData.append(str(latitude))
    latLongData.append(str(longitude))
    geolocator = Nominatim(user_agent="GetLoc")
    location = geolocator.reverse(", ".join(latLongData))
    city = result.city
    while True:
        if city == None:
            print("Unfortunatelly there is no access to your location via Your IP address.")
            break
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*len(str(location)))
        print(location)
        print("="*len(str(location)))
        print("Are You satisfied with search results?")
        print("(0) Yes")
        print("(1) No")
        choice = CheckInputInt()
        match choice:
            case 0:
                data = location.raw
                addressList.insert(0, data['address']['country'])
                addressList.insert(1, data['address']['city'])
                addressList.insert(2, data['address']['road'])
                try:
                    addressList.append(3, data['address']['house_number'])
                except:
                    pass
                YourLocation = YourAddress(latitude, longitude, data)
                return YourLocation
            case 1:
                break
            case 'exit':
                exit()

def EnterYourLocation():
    country = "Poland"
    city = None
    street = None
    number = None
    addressList.insert(0, country)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==================================")
        print("(0) Return")
        print("(1) Add the name of the city/town")
        print("(2) Add the name of the street")
        print("(3) Add the number of the building")
        if city != None and street != None:
            prGreen("(4) Continue")         
        print("==================================")
        choice = CheckInputForExit()
        if (city == None or street == None) and choice == 4:
            choice = 5
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==================================")
        match choice:
            case 0:
                break
            case 1:
                if city != None:
                    text = "Previous name of the city: " + city
                    prRed(text)
                    addressList.remove(city)
                print("Add the name of the city/town:")
                city = input()
                addressList.insert(1, city)
            case 2:
                if street != None:
                    text = "Previous name of the street: " + street
                    prRed(text)
                    addressList.remove(street)
                print("Add the name of the street:")
                street = input()
                addressList.insert(2, street)
            case 3:
                if number != None:
                    text = "Previous number of the building: " + number
                    prRed(text)
                    addressList.remove(number)
                print("Add the number of the building: ")
                number = input()
                addressList.insert(3, number)
            case 4:
                break
            case "exit":
                exit()
    if choice == 4:
        os.system('cls' if os.name == 'nt' else 'clear')
        address = ", ".join(addressList)
        print(address)
        location = geolocator.geocode(address, addressdetails=True)
        data = location.raw
        YourLocation = YourAddress(location.latitude, location.longitude, data)
        return YourLocation

def Menu(YourLocation):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("================Choose:===================")
        print("(0) Check your database")
        print("(1) Add a new shop to Your database")
        print("(2) Find all shops in Your area")
        print("(3) Find the most suitable shop")
        print("(4) Change Your location")
        print("(5) Return - change Your Location entirely")
        print("(6) Exit")
        choice = CheckInputForExit()
        os.system('cls' if os.name == 'nt' else 'clear')
        match choice:
            case 0:
                CheckYourDatabase(YourLocation)          
            case 1:
                YourShop = AddShop(YourLocation)
                if YourShop:
                    listOfAllShops.append(YourShop)
                    UploadData()
            case 2:
                radius = YourLocation.AreaMenu()
                if type(radius) == str:
                    YourLocation.findShopsArea(radius, 1)
                elif radius and type(radius) == float:
                    YourLocation.findShopsArea(radius, 0)                 
                elif not radius:
                    pass
            #case 3:
            case 4:
                YourLocation = ChangeData(YourLocation)
            case 5:
                return 0
            case 6:
                exit()
            case 'exit':
                exit()


def ChangeData(YourLocation):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*len(", ".join(addressList)))
        print(", ".join(addressList))
        print("="*len(", ".join(addressList)))
        print("(0) Change the city/town")
        print("(1) Change the street")
        print("(2) Change the number of the building")
        print("(3) Return")
        choice = CheckInputForExit()
        os.system('cls' if os.name == 'nt' else 'clear')
        match choice:
            case 0:
                print("You entered before:", YourLocation.data['address']['city'])
                print("="*(len(YourLocation.data['address']['city'])//2), "Add a new city/town:", "="*(len(YourLocation.data['address']['city'])//2))
                city = input()
                addressList.remove(addressList[1])
                addressList.insert(1, city)
            case 1:
                print("You entered before:", YourLocation.data['address']['road'])
                print("="*(len(YourLocation.data['address']['road'])//2), "Add a new street", "="*(len(YourLocation.data['address']['road'])//2))
                street = input()
                addressList.remove(addressList[2])
                addressList.insert(2, street)
            case 2:
                try:
                    print("You entered before:", addressList[3])
                    print("="*(len(addressList[3])//2), "Add a new number of the building:", "="*(len(addressList[3])//2))
                    addressList.remove(addressList[3])
                except:
                    print("Add the number of the building:")
                number = input()
                addressList.insert(3, number)
            case 3:
                break
            case 'exit':
                exit() 
        address = ", ".join(addressList) 
        print(address)
        location = geolocator.geocode(address, addressdetails=True)
        YourLocation.data = location.raw
        YourLocation.latitude = location.latitude
        YourLocation.longitude = location.longitude
        return YourLocation

def AddShop(YourLocation):
    country = "Poland"
    city = None
    street = None
    number = None
    deliveryday = None
    name = None
    prices = {}
    addressShop.insert(0, country)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==================================")
        print("(0) Return")
        print("(1) Add the name of the shop")
        print("(2) Add the name of the city/village")
        print("(3) Add the name of the street")
        print("(4) Add the number of the building")
        print("(5) Enter the delivery day")
        print("(6) Enter prices")
        if city != None and street != None and number != None and name != None:
            prGreen("(7) Continue")         
        print("==================================")
        choice = CheckInputForExit()
        if (city == None or street == None or name == None or number == None) and choice == 7:
            choice = 9
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==================================")
        match choice:
            case 0:
                break
            case 1:
                if name != None:
                    text = "Previous name of the shop: "+ name
                    prRed(text)
                print("Add the name of the shop:")
                name = input()
            case 2:
                if city != None:
                    text = "Previous name of the city/village: " + city
                    prRed(text)
                    addressShop.remove(city)
                print("Add the name of the city/village:")
                city = input()
                addressShop.insert(1, city)
            case 3:
                if street != None:
                    text = "Previous name of the street: " + street
                    prRed(text)
                    addressShop.remove(street)
                print("Add the name of the street:")
                street = input()
                addressShop.insert(2, street)
            case 4:
                if number != None:
                    text = "Previous number of the building: " + number
                    prRed(text)
                    addressShop.remove(number)
                print("Add the number of the building: ")
                number = input()
                addressShop.insert(3, number)
            case 5:
                if deliveryday != None:
                    text = "Previous delivery day: " + deliveryday
                    prRed(text)
                    time.sleep(2)
                deliveryday = AddDeliveryDay(deliveryday)
            case 6:
                prices = AddPrices(prices)
            case 7:
                break
            case "exit":
                exit()
    if choice == 7:
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            address = ", ".join(addressShop)
            print(name)
            print(address)
            print("Delivery day: ", deliveryday)
            for key, value in prices.items():
                print(key, ":", value)
            location = geolocator.geocode(address, addressdetails=True)
            data = location.raw
        except:
            print("There is no such location")
            time.sleep(4)
            return 0
        if deliveryday == None:
            deliveryday = "unspecified"
        YourShop = Shops(name, location.latitude, location.longitude, data, deliveryday, prices)
        for shop in listOfAllShops:
            if name == shop.name and shop.data['address']['road'] == data['address']['road'] and YourShop == shop:
                print("You already have this shop in Your database")
                print("(0) Return")
                print("(1) Check details of the shop")
                choice = CheckInputForExit()
                match choice:
                    case 0:
                        return 0
                    case 1:
                        YourShop.DisplayDetailsOfShop(YourLocation)
                    case 'exit':
                        exit()
        time.sleep(3)
        return YourShop

def AddDeliveryDay(delivery):
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
        choice = CheckInputForExit()
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
            case 'exit':
                exit() 
        print("Delivery day: ", delivery)
        time.sleep(2)
        return delivery

def AddPrices(prices):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        for key, value in prices.items():
            print(key, ":", value)
        print("===================================================")
        print("(0) Add prices for each day of the week")
        print("(1) Add a note - prices are different for each item")
        print("(2) Return")
        choice = CheckInputForExit()       
        match choice:
            case 0:
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    for key, value in prices.items():
                        print(key, ":", value)
                    print("===========================")
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
                            if monday != "0":
                                prices['Monday'] = monday
                        case 1:
                            print("Enter the prize per kg on Tuesday or (0) return")
                            tuesday = input()
                            if tuesday != "0":
                                prices['Tuesday'] = tuesday
                        case 2:
                            print("Enter the prize per kg on Wednesday or (0) return")
                            wednesday = input()
                            if wednesday != "0":
                                prices['Wednesday'] = wednesday
                        case 3:
                            print("Enter the prize per kg on Thursday or (0) return")
                            thursday = input()
                            if thursday != "0":
                                prices['Thursday'] = thursday
                        case 4:
                            print("Enter the prize per kg on Friday or (0) return")
                            friday = input()
                            if friday != "0":
                                prices['Friday'] = friday
                        case 5:
                            print("Enter the prize per kg on Saturday or (0) return")
                            saturday = input()
                            if saturday != "0":
                                prices['Saturday'] = saturday
                        case 6:
                            print("Enter the prize per kg on Sunday or (0) return")
                            sunday = input()
                            if sunday != "0":
                                prices['Sunday'] = sunday
                        case 7:
                            break
            case 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                prices = {'Monday': "unspecified",'Tuesday': "unspecified", 'Wednesday': "unspecified", 'Thursday': "unspecified", 'Firday': "unspecified", 
                                'Saturday': "unspecified", 'Sunday': "unspecified"}
                print("Note added")
                time.sleep(2)
            case 2:
                return prices
            case 'exit':
                exit()

def CheckYourDatabase(YourLocation):
     while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(len(listOfAllShops)):
            try:
                try:
                    print("({}) - {}: {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'], 
                    listOfAllShops[i].data['address']['road'], listOfAllShops[i].data['address']['house_number']))
                except:
                    print("({}) - {}: {}, {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'],
                    listOfAllShops[i].data['address']['road']))
            except:
                try:
                    print("({}) - {}:  {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road'], 
                    listOfAllShops[i].data['address']['house_number']))
                except:
                     print("({}) - {}: {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road']))
        print("=========================================")
        if len(listOfAllShops) == 0:
            print("(0) Add a new shop to Your database")
            print("(1) Return")
        else:
            print("(0) Check for details of a shop")
            print("(1) Add a new shop to Your database")
            print("(2) Remove a shop from Your database")
            print("(3) Return")
        choice = CheckInputForExit()
        if len(listOfAllShops) == 0:
            if choice == 0:
                choice = 1
            elif choice == 1:
                choice = 3
            elif type(choice) == int:
                if choice>= 2:
                    choice = 4
        os.system('cls' if os.name == 'nt' else 'clear')
        match choice:
            case 0:
                for i in range(len(listOfAllShops)):
                    try:
                        try:
                            print("({}) - {}: {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'], 
                            listOfAllShops[i].data['address']['road'], listOfAllShops[i].data['address']['house_number']))
                        except:
                            print("({}) - {}: {}, {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'],
                            listOfAllShops[i].data['address']['road']))
                    except:
                        try:
                            print("({}) - {}:  {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road'], 
                            listOfAllShops[i].data['address']['house_number']))
                        except:
                            print("({}) - {}: {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road']))
                print("(0) Return")
                print("Enter an index of a shop to see its details:")
                id = CheckInputInt()
                if id == 0:
                    pass
                else:
                    while 0>id> len(listOfAllShops):
                        print("Try again: ")
                        id = CheckInputInt()
                    listOfAllShops[id-1].DisplayDetailsOfShop(YourLocation)
            case 1:
                YourShop = AddShop(YourLocation)
                if YourShop:
                    listOfAllShops.append(YourShop)
                    UploadData()
            case 2:
                RemoveShopFromDatabase()
            case 3:
                break
            case 'exit':
                exit()

def RemoveShopFromDatabase():
    print("(0) Return")
    print("Enter an index of a shop to remove from Your database")
    for i in range(0,len(listOfAllShops)):
        try:
            try:
                print("({}) - {}: ".format(i+1, listOfAllShops[i].name), listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'], 
                listOfAllShops[i].data['address']['road'], listOfAllShops[i].data['address']['house_number'])
            except:
                print("({}) - {}: ".format(i+1, listOfAllShops[i].name), listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'],
                listOfAllShops[i].data['address']['road'])
        except:
            try:
                print("({}) - {}: ".format(i+1, listOfAllShops[i].name), listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road'], 
                listOfAllShops[i].data['address']['house_number'])
            except:
                print("({}) - {}: ".format(i+1, listOfAllShops[i].name), listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road'])
    id = CheckInputForExit()
    if not id:
        return
    if id == "exit":
        exit()
    while 0>id>len(listOfAllShops):
        print("Try again: ")
        id = CheckInputInt()
    listOfAllShops.remove(listOfAllShops[id-1])
    UploadData()
class YourAddress:
    def __init__(self, latitude, longitude, data):
        self.latitude = latitude
        self.longitude = longitude
        self.data = data
    def AreaMenu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("====================Choose:=====================")
            print("(0) Enter the maximum distance to search in (KM)")
            print("(1) Search via the district")
            print("(2) Return")
            choice = CheckInputForExit()
            os.system('cls' if os.name == 'nt' else 'clear')
            match choice:
                case 0:
                    radius = self.AreaKm()
                    if radius:
                        return radius
                    elif not radius:
                        pass
                case 1:
                    radius = self.AreaDistrict()
                    if radius:
                        return radius
                    elif not radius:
                        pass
                case 2:
                    return 0
                case 'exit':
                    exit()
    def AreaKm(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Enter the distance in Km or (0) return:")
            return CheckInputFloat()
    def AreaDistrict(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("(0) Return")
            print("(1) Choose the district You are currently in")
            print("(2) Choose another district in this city")
            choice = CheckInputForExit()
            match choice:
                case 0:
                    return 0
                case 1:
                    return self.data['address']['suburb']
                case 2:
                    addressChoice = []
                    os.system('cls' if os.name == 'nt' else 'clear')
                    addressChoice.append("Poland")
                    addressChoice.append(self.data['address']['city'])
                    addressChoice.append(input())
                    address = ", ".join(addressChoice)
                    location = geolocator.geocode(address, addressdetails=True)
                    if location.raw['address']['suburb'] == addressChoice[-1]:
                        return addressChoice[-1]
                    else:
                        print("There is no such district")
                        time.sleep(2)
                        break
                case 'exit':
                    exit()
    def findShopsArea(self, district, string):
        global newLocations
        global listOfAllShops
        closestDatabase = []
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Please wait...")
        if string:
            address1 = ", ".join(["second hand", district, self.data['address']['city']])
            address2 = ", ".join(["używana odzież", district, self.data['address']['city']])
            address3 = ", ".join(["lumpeks", district, self.data['address']['city']])
            address4 = ", ".join(["sklep odzież", district, self.data['address']['city']])
            address5 = ", ".join(["sklep z ubraniami używanymi", district, self.data['address']['city']])
            address6 = ", ".join(["lump", district, self.data['address']['city']])
            address7 = ", ".join(["sklep z odzieżą używaną", district, self.data['address']['city']])
            address8 = ", ".join(["sklep z odzieżą", "lumpeks", district, self.data['address']['city']])
            address9 = ", ".join(["sklep odzieżowy", "używana", district, self.data['address']['city']])
            address10 = ", ".join(["lumpex", district, self.data['address']['city']])
            address11 = ", ".join(["używana", district, self.data['address']['city']])
            address12 = ", ".join(["vintage", "sklep z odzieżą używaną", district, self.data['address']['city']])
            address13 = ", ".join(["sklep", "odzież", "używana", district, self.data['address']['city']])
            address14 = ", ".join(["sklep odzieżowy", "lumpeks", district, self.data['address']['city']])
            address15 = ", ".join(["second hand shop", district, self.data['address']['city']])
            address16 = ", ".join(["komis", "sklep z odzieżą używaną", district, self.data['address']['city']])
        else:
            address1 = ", ".join(["second hand", self.data['address']['city']])
            address2 = ", ".join(["używana odzież", self.data['address']['city']])
            address3 = ", ".join(["lumpeks", self.data['address']['city']])
            address4 = ", ".join(["sklep odzież", self.data['address']['city']])
            address5 = ", ".join(["sklep z ubraniami używanymi", self.data['address']['city']])
            address6 = ", ".join(["lump", self.data['address']['city']])
            address7 = ", ".join(["sklep z odzieżą używaną", self.data['address']['city']])
            address8 = ", ".join(["sklep z odzieżą", "lumpeks", self.data['address']['city']])
            address9 = ", ".join(["sklep odzieżowy", "używana", self.data['address']['city']])
            address10 = ", ".join(["lumpex", self.data['address']['city']])
            address11 = ", ".join(["używana", self.data['address']['city']])
            address12 = ", ".join(["vintage", "sklep z odzieżą używaną", self.data['address']['city']])
            address13 = ", ".join(["sklep", "odzież", "używana", self.data['address']['city']])
            address14 = ", ".join(["sklep odzieżowy", "lumpeks", self.data['address']['city']])
            address15 = ", ".join(["second hand shop", self.data['address']['city']])
            address16 = ", ".join(["komis", "sklep z odzieżą używaną", self.data['address']['city']])
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
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location2:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location3:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location4:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location5:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location6:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location7:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location8:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location9:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location10:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location11:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location12:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location13:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location14:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location15:
                newLocations.append(loc)
        except:
            pass
        try:
            for loc in location16:
                newLocations.append(loc)
        except:
            pass
        if not string:
            self.CheckDistanceFromShop(district)
        if string:
            for loc in listOfAllShops:
                if loc.data['address']['suburb'] == district and not(loc in closestDatabase):
                    closestDatabase.append(loc)
            self.OperateOnFoundLocations(closestDatabase)
    def CheckDistanceFromShop(self, radius):
        global newLocations
        global listOfAllShops
        distance = []
        distanceDatabase = []
        closestDistance = []
        closestDatabase = []
        for loc in newLocations:
            distance.append(GD((str(loc.latitude),str(loc.longitude)), (self.latitude,self.longitude)).km)
        for id in range(len(newLocations)):
            if distance[id] <= radius and not (newLocations[id] in closestDistance):
                closestDistance.append(newLocations[id])
        for loc in listOfAllShops:
            distanceDatabase.append(GD((str(loc.latitude),str(loc.longitude)), (self.latitude,self.longitude)).km)
        for id in range(len(listOfAllShops)):
            if distanceDatabase[id] <= radius and not (listOfAllShops[id] in closestDatabase):
                closestDatabase.append(listOfAllShops[id])
        newLocations.clear()
        newLocations = closestDistance
        self.OperateOnFoundLocations(closestDatabase)
    def OperateOnFoundLocations(self, closestDatabase):
        global newLocations
        global listOfAllShops
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if len(newLocations) != 0:
                print("New locations within given distance:")
                for i in range(len(newLocations)):
                    print("({}) - ".format(i), newLocations[i])
            if len(closestDatabase) != 0:
                print("Locations from Your database within given distance:")
                for i in range(len(closestDatabase)):
                    address = ", ".join(closestDatabase[i].data['address'].values())
                    print("({}) - {}: ".format(i+1, closestDatabase[i].name), address)
            if len(newLocations) != 0 or len(closestDatabase) != 0:
                print("================================================")
                print("(0) Check for details (only shops from database)")
                print("(1) Add a new found shop to Your database")
                print("(2) Return")
                choice = CheckInputForExit()
            else:
                print("There are no shops within your reach")
                print("================================================")
                time.sleep(2)
                break
            match choice:
                case 0:
                    self.DetailsShopsDatabaseInDistance(closestDatabase)
                case 1:
                    self.AddFoundShop()
                case 2:
                    newLocations.clear()
                    break
                case 'exit':
                    exit()
    def AddFoundShop(self):
        global newLocations        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("New locations within given distance:")
        for i in range(len(newLocations)):
            print("({}) - ".format(i+1), newLocations[i])
        print("Enter index of a new shop You would like to add or (0) return:")
        id = CheckInputForExit()
        if id == 0:
            return
        elif id == 'exit':
            exit()
        print(newLocations[id-1])
        addressShop = []
        checkBox = [0,0,0,0]
        addressShop.insert(0, "Poland")
        #name = newLocations[id-1][0]
        #city = newLocations[id-1][6]
        #street = newLocations[id-1][2]
        #number = newLocations[id-1][1]
        prices = {}
        deliveryday = None
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("(0) Return")
            print("(1) Add the name of the shop")
            print("(2) Add the name of the city/town")
            print("(3) Add the name of the street")
            print("(4) Add the number of the building")
            print("(5) Enter the delivery day")
            print("(6) Enter prices")         
            if checkBox[0] and checkBox[1] and checkBox[2] and checkBox[3]:
                prGreen("(7) Continue")         
            print("==================================")
            choice = CheckInputForExit()
            if (0 in checkBox) and choice == 7:
                choice = 9
            os.system('cls' if os.name == 'nt' else 'clear')
            print("==================================")
            match choice:
                case 0:
                    break
                case 1:                    
                    text = "Previous name of the shop: "+ name
                    prRed(text)
                    print("Add the name of the shop:")
                    name = input()
                    checkBox.insert(1, 1)
                case 2:
                    text = "Previous/default name of the city/village: "+ city
                    prRed(text)
                    print("Add the name of the city/village")
                    city = input()
                    addressShop.insert(1, street)
                    checkBox.insert(2, 1)
                case 3:
                    text = "Previous name of the street: " + street
                    prRed(text)
                    addressShop.remove(street)
                    print("Add the name of the street:")
                    street = input()
                    addressShop.insert(2, street)
                    checkBox.insert(3, 1)
                case 4:
                    text = "Previous number of the building: " + number
                    prRed(text)
                    addressShop.remove(number)
                    print("Add the number of the building: ")
                    number = input()
                    addressShop.insert(3, number)
                    checkBox.insert(0, 1)
                case 5:
                    if deliveryday != None:
                        text = "Previous delivery day: " + deliveryday
                        prRed(text)
                        time.sleep(2)
                    deliveryday = AddDeliveryDay(deliveryday)
                case 6:
                    prices = AddPrices(prices)
                case 7:
                    break
                case "exit":
                    exit()
        if choice == 7:
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                address = ", ".join(addressShop)
                print(name)
                print(address)
                print("Delivery day: ", deliveryday)
                for key, value in prices.items():
                    print(key, ":", value)
                location = geolocator.geocode(address, addressdetails=True)
                data = location.raw
            except:
                print("There is no such location")
                time.sleep(4)
                return 0
            if deliveryday == None:
                deliveryday = "unspecified"
            YourShop = Shops(name, location.latitude, location.longitude, data, deliveryday, prices)
            for shop in listOfAllShops:
                if name == shop.name and shop.data['address']['road'] == data['address']['road'] and YourShop == shop:
                    print("You already have this shop in Your database")
                    print("(0) Return")
                    print("(1) Check details of the shop")
                    choice = CheckInputForExit()
                    match choice:
                        case 0:
                            return 0
                        case 1:
                            YourShop.DisplayDetailsOfShop(self)
                        case 'exit':
                            exit()
            time.sleep(3)
            return YourShop




    def DetailsShopsDatabaseInDistance(self, closestDatabase):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Locations from Your database within given distance:")
            for i in range(len(closestDatabase)):
                address = ", ".join(closestDatabase[i].data['address'].values())
                print("({}) - {}: ".format(i+1, closestDatabase[i].name), address)
            print("Enter the index of a shop to check or (0) return: ")
            id = CheckInputForExit()
            if not id:
                break
            if id == 'exit':
                exit()
            if id>0:
                closestDatabase[id-1].DisplayDetailsOfShop(self)


class Shops:
    def __init__(self, name, latitude, longitude, data, delivery, prices):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.data = data
        self.delivery = delivery
        self.prices = prices
    def DisplayDetailsOfShop(self, YourLocation):
        os.system('cls' if os.name == 'nt' else 'clear')
        distance = GD((self.latitude, self.longitude), (YourLocation.latitude, YourLocation.longitude)).km
        print("Name: {} - currently {} km from You".format(self.name, "%.3f" % distance))
        try:
            try:
                print("Address: ", self.data['address']['city'], self.data['address']['suburb'], 
                self.data['address']['road'], self.data['address']['house_number'])
            except:
                print("Address: ", self.data['address']['city'], self.data['address']['suburb'], 
                self.data['address']['road'])
        except:
            try:
                print("Address: ", self.data['address']['village'], self.data['address']['road'], self.data['address']['house_number'])
            except:
                print("Address: ", self.data['address']['village'], self.data['address']['road'])
        print((len(self.delivery))//2*"="+"Prices"+(len(self.delivery))//2*"=")  #finish
        for key, value in self.prices.items():
            print(key, ":", value)
        print("Day of delivery: ", self.delivery)
        print("================="+len(self.delivery)*"=")
        print("(0) Return")
        choice = CheckInputForExit()
        while True:
            match choice:
                case 0:
                    break
                case 'exit':
                    exit()
        
            
def LoadData():
    global listOfAllShops 
    try:
        with open('shopsData.pkl', 'rb') as shopsData:
            listOfAllShops = pickle.load(shopsData)
    except:
        print("You have 0 shops in Your database")

def UploadData():
    with open('shopsData.pkl', 'wb') as shopsData:
        pickle.dump(listOfAllShops, shopsData)          

Main()