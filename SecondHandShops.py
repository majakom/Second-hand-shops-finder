import pickle
import time
import os
import json
from urllib.request import urlopen
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.geocoders import Nominatim
from geopy.distance import geodesic as GD
from datetime import date
try:
    geolocator = Nominatim(user_agent="GetLoc")
except:
    print("Your internet connection is unstable")
    exit()
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
                try:
                    addressList.insert(1, data['address']['city'])
                except:
                    try:
                        addressList.insert(1, data['address']['village'])
                    except:
                        addressList.insert(1, data['address']['town'])
                try:
                    addressList.insert(2, data['address']['road'])
                except:
                    addressList.insert(2, data['address']['neighbourhood'])
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
        print("(3) Add the house number")
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
                    text = "Previous house number: " + number
                    prRed(text)
                    addressList.remove(number)
                print("Add the house number: ")
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
        try:
            location = geolocator.geocode(address, addressdetails=True)
            data = location.raw
            print(data)
            input()
            YourLocation = YourAddress(location.latitude, location.longitude, data)
            return YourLocation
        except:
            print("There is no such location/Your internet connection is unstable")
            exit()
        

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
            case 3:
                FindBestShopOptions(YourLocation)
            case 4:
                YourLocation = ChangeData(YourLocation)
            case 5:
                return 0
            case 6:
                exit()
            case 'exit':
                exit()

def FindBestShopOptions(YourLocation):
    options = [None, None, None]
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Choose properties that You want to include:")
        print("(0) Distance - find the closest shop")
        print("(1) Day of delivery")
        print("(2) Price")
        print("(3) Return")
        print("(4) Continue")
        choice = CheckInputForExit()
        match choice:
            case 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Enter the max distance from You in km or (0) return:")
                km = CheckInputFloat()
                if km != 0:
                    options[0] = km
            case 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Choose an option:")
                print("(0) Find a shop with the newest products (with the most recent delivery)")
                print("(1) Find a shop where delivery is going to be soon (in a day/two, etc.)")
                print("(2) Return - do not include option \"day of delivery\" in search for the most suitable shop" )
                choice = CheckInputForExit()
                os.system('cls' if os.name == 'nt' else 'clear')
                match choice:
                    case 0:
                        options[1]= 1
                    case 1:
                        options[1] = 2
                    case 2:
                        pass
                    case 'exit':
                        exit()
            case 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Choose an option:")
                print("(0) Find a shop where prices per kilogram of product are the lowest")
                print("(1) Find a shop where prices per kilogram of product are the highest")
                print("(2) Find a shop where prices are different for each product")
                print("(3) Return - do not include option \"price\" in search for the most suitable shop")
                choice = CheckInputForExit()
                match choice:
                    case 0:
                        options[2] = 1
                    case 1:
                        options[2] = 2
                    case 2:
                        options[2] = 3
                    case 3:
                        pass
                    case 'exit':
                        exit()
            case 3:
                break
            case 4:
                FindBestShop(YourLocation, options)
            case 'exit':
                exit()
        print("You chose: ")
        for i in range(len(options)):
            if options[i] == None:
                print(i)

def FindBestShop(YourLocation, options):
    os.system('cls' if os.name == 'nt' else 'clear')
    global listOfAllShops
    distdelRecentUnspecified = []
    distdelSoonUnspecified = []
    distdelSoon = []
    distdelRecent = []
    distanceCheck = []
    deliveryRecent = []
    deliverySoon =[]
    distanceAndPrices = set()
    distPriceUnspecified = []
    PriceUnspecified = []
    distPriceOutput = []
    deliverySoonDistance = []
    deliveryRecentDistance = []
    PricesOnly = set()
    LowestPrice = []
    HighestPrice = []
    LowPriceRecentDeliver = []
    HighPriceRecentDeliver = []
    LowPriceSoonDeliver = []
    HighPriceSoonDeliver = []
    RecentUnspecified = []
    SoonUnspecified = []
    distdelRecentExp = []
    distdelSoonExp = []
    distdelRecentCheap = []
    distdelSoonCheap = []
    today = date.today()
    week = ['Monday','Tuesady', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    getDay = date.weekday(today)
    dayOfWeek = week[getDay]
    #checking for distance
    if options[0] != None:
        if options[0]>0:
            for loc in listOfAllShops:
                dist = GD((str(loc.latitude),str(loc.longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                if dist <= options[0] and not(loc in distanceCheck):
                    distanceCheck.append(loc)
            if len(distanceCheck) == 0:
                print("There are no shops within this area")
                time.sleep(2)
                options = []
                return options

    #only distance
    if options[0] != None: 
        if options[0]>0 and options[1] == None and options[2] == None:
            for i in range(len(distanceCheck)):
                dist = GD((str(distanceCheck[i].latitude),str(distanceCheck[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                if distanceCheck[i].prices[dayOfWeek] !=0 and distanceCheck[i].prices[dayOfWeek] == 'unspecified':                
                    print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,distanceCheck[i].name, "%.3f" % dist, distanceCheck[i].prices[dayOfWeek],distanceCheck[i].delivery))
                elif distanceCheck[i].prices[dayOfWeek] != 'unspecified':
                    print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,distanceCheck[i].name, "%.3f" % dist, distanceCheck[i].prices[dayOfWeek], distanceCheck[i].delivery))
            print("==============Choose an option================")
            print("(0) Return")
            print("(1) Display details of a shop")
            choice = CheckInputForExit()
            match choice:
                case 0:
                    return
                case 1:
                    print("Enter an id of a shop:")
                    id = CheckInputInt()
                    while id>= len(distanceCheck):
                        print("Try again:")
                        id = CheckInputInt()
                    distanceCheck[id].DisplayDetailsOfShop(YourLocation)
                case 'exit':
                    exit()


    #checking for cheapest/most expensive shop or of unspecified prices in certain area:
    if options[0] != None:
        if options[0]>0 and (options[2] == 1 or options[2] == 2 or options[2] ==3) and options[1] == None:
            for loc in distanceCheck:
                if loc.prices[dayOfWeek] and loc.prices[dayOfWeek] != 'unspecified':
                    distanceAndPrices.add(loc.prices[dayOfWeek])
                if loc.prices[dayOfWeek] == 'unspecified':
                    distPriceUnspecified.append(loc)
            #finding cheapest shop in a distance
            if options[2] == 1 and len(distanceAndPrices)!=0:
                list(distanceAndPrices).sort()
                print(distanceAndPrices)
                input()
                count = 0
                for i in range(len(distanceAndPrices)):
                    for val in range(len(distanceCheck)):
                        if distanceCheck[val].prices[dayOfWeek] == int(list(distanceAndPrices)[i]):
                            if distanceCheck[val].prices[dayOfWeek] != 0 and not (distanceCheck[val] in distPriceOutput):
                                distPriceOutput.append(distanceCheck[val])
                                if (count==10 and i!=0) or (count>10 and i==1):
                                    break
                                count+=1
            #finding most expensive shop in a distance
            if options[2] == 2 and len(distanceAndPrices)!=0:
                distanceAndPrices = list(distanceAndPrices).sort(reverse = True)
                count = 0
                for i in range(len(distanceAndPrices)):
                    for val in range(len(distanceCheck)):
                        if distanceCheck[val].prices[dayOfWeek] == distanceAndPrices[i]:
                            if distanceCheck[val].prices[dayOfWeek] != 0 and  not (distanceCheck in distPriceOutput):
                                distPriceOutput.append(distanceCheck[val])
                                if (count==10 and i!=0) or (count>10 and i==1):
                                    break
                                count+=1
                
            #unspecified price in a distance
            if options[2] == 3:
                if len(distPriceUnspecified) == 0:
                    print("There are no shops within this area")
                    time.sleep(2)
                    options = []
                    return options
                for i in range(len(distPriceUnspecified)):
                    dist = GD((str(distPriceUnspecified[i].latitude),str(distPriceUnspecified[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                    print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,distPriceUnspecified[i].name, "%.3f" % dist, distPriceUnspecified[i].prices[dayOfWeek], distPriceUnspecified[i].delivery))
                print("==============Choose an option================")
                print("(0) Return")
                print("(1) Display details of a shop")
                choice = CheckInputForExit()
                match choice:
                    case 0:
                        return
                    case 1:

                        print("Enter an id of a shop:")
                        id = CheckInputInt()
                        while id>= len(distPriceUnspecified):
                            print("Try again:")
                            id = CheckInputInt()
                        distPriceUnspecified[id].DisplayDetailsOfShop(YourLocation)
                    case 'exit':
                        exit()
            else:
                if len(distanceAndPrices) == 0:
                    print("There are no shops within this area")
                    time.sleep(2)
                    options = []
                    return options
                elif len(distPriceOutput) == 0:
                    print("There are no shops within this area")
                    time.sleep(2)
                    options = []
                    return options
                for i in range(len(distPriceOutput)):
                    dist = GD((str(distPriceOutput[i].latitude),str(distPriceOutput[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                    print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,distPriceOutput[i].name, "%.3f" % dist, distPriceOutput[i].prices[dayOfWeek], distPriceOutput[i].delivery))
                print("==============Choose an option================")
                print("(0) Return")
                print("(1) Display details of a shop")
                choice = CheckInputForExit()
                match choice:
                    case 0:
                        return
                    case 1:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("Enter an id of a shop:")
                        id = CheckInputInt()
                        while id>= len(distPriceOutput):
                            print("Try again:")
                            id = CheckInputInt()
                        distPriceOutput[id].DisplayDetailsOfShop(YourLocation)
                    case 'exit':
                        exit()


    #checking for delivery day
    if options[1] == 1 or options[1] == 2:
        for loc in listOfAllShops:
            if loc.delivery == week[getDay-1] or loc.delivery == week[getDay-2]  or loc.delivery == week[getDay-3]:
                deliveryRecent.append(loc)
            if loc.delivery == week[getDay-6] or loc.delivery == week[getDay-5]  or loc.delivery == week[getDay-4]:
                deliverySoon.append(loc)
            if len(deliverySoon) == 0 or len(deliveryRecent) == 0:
                print("There are no shops with requested delivery day assigned")
                options = []
                return
            
    #only for delivery day
    #delivery recent
    if options[1] == 1 and options[2] == None and options[0] == None:
        for i in range(len(deliveryRecent)):
            dist = GD((str(deliveryRecent[i].latitude),str(deliveryRecent[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
            if deliveryRecent[i].prices[dayOfWeek] == 'unspecified':                
                print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,deliveryRecent[i].name, dist, deliveryRecent[i].prices[dayOfWeek], deliveryRecent[i].delivery))
            elif len(deliveryRecent[i].price[dayOfWeek]) != 0:
                print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,deliveryRecent[i].name, dist, deliveryRecent[i].prices[dayOfWeek], deliveryRecent[i].delivery))
    #delivery soon
    if options[1] == 2  and options[2] == None and options[0] == None:
        for i in range(len(deliverySoon)):
            dist = GD((str(deliverySoon[i].latitude),str(deliverySoon[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
            if deliverySoon[i].price[dayOfWeek] == 'unspecified':                
                print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,deliverySoon[i].name, dist, deliverySoon[i].prices[dayOfWeek], deliverySoon[i].delivery))
            elif len(deliverySoon[i].prices[dayOfWeek]) != 0:
                print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,deliverySoon[i].name, dist, deliverySoon[i].prices[dayOfWeek], deliverySoon[i].delivery))

    # checking for delivery and distance:
    if options[0] != None:
        if options[0]>0 and (options[1] == 1 or options[1] == 2) and options[2] == None:
            #checking for recent delivery in distance
            if options[1] ==1:
                for i in range(len(distanceCheck)):
                    if (deliveryRecent[i] in distanceCheck) and not(deliveryRecent[i] in deliveryRecentDistance):
                        deliveryRecentDistance.append(deliveryRecent[i])
                if len(deliveryRecentDistance) == 0:
                    print("There is no such shop")
                    options = []
                    return
                else:
                    dist = GD((str(deliveryRecentDistance[i].latitude),str(deliveryRecentDistance[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                    if deliveryRecentDistance[i].prices[dayOfWeek] == 'unspecified':                
                        print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,deliveryRecentDistance[i].name, dist, deliveryRecentDistance[i].price[dayOfWeek],
                                                                                            deliveryRecentDistance[i].delivery))
                    elif len(deliveryRecentDistance[i].prices[dayOfWeek]) != 0:
                        print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,deliveryRecentDistance[i].name, dist, deliveryRecentDistance[i].prices[dayOfWeek], 
                                                                                                deliveryRecentDistance[i].delivery))
            #checking for soon delivery in distance
            if options[1] == 2:
                for i in range(len(distanceCheck)):
                    if (deliverySoon[i] in distanceCheck) and not(deliverySoon[i] in deliverySoonDistance):
                        deliverySoonDistance.append(deliverySoon[i])
                if len(deliverySoonDistance) == 0:
                    print("There is no such shop")
                    options = []
                    return
                else:
                    dist = GD((str(deliverySoonDistance[i].latitude),str(deliverySoonDistance[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                    if deliveryRecentDistance[i].prices[dayOfWeek] == 'unspecified':                
                        print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,deliverySoonDistance[i].name, dist, deliverySoonDistance[i].prices[dayOfWeek],
                                                                                            deliverySoonDistance[i].delivery))
                    elif len(deliverySoonDistance[i].prices[dayOfWeek]) != 0:
                        print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,deliverySoonDistance[i].name, dist, deliverySoonDistance[i].prices[dayOfWeek], 
                                                                                                deliverySoonDistance[i].delivery))
    #checking for price unspecified:
    if options[2] == 3:
        for loc in listOfAllShops:
            if loc.prices[dayOfWeek] == 'unspecified':
                PriceUnspecified.append(loc)
        if len(PriceUnspecified) == 0:
            print("There is no such shop")
            options = []
            return
        
    #checking for price values:
    if (options[2] == 1 or options[2] == 2) and options[1] == None and options[0] == None:
        for loc in listOfAllShops:
            PricesOnly.add(loc.prices[dayOfWeek])
        #checking for lowest price
        if options[2] == 1:
            list(PricesOnly).sort()
            count = 0
            for i in list(PricesOnly):
                for val in range(len(listOfAllShops)):
                    if listOfAllShops[val].prices[dayOfWeek] == PricesOnly[i]:
                        LowestPrice.append(listOfAllShops[val])
                        count +=1
                        if count == 10:
                            break
            if len(LowestPrice) == 0:
                options = []
                return
            for i in range(len(LowestPrice)):
                dist = GD((str(LowestPrice[i].latitude),str(LowestPrice[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                if LowestPrice[i].price[dayOfWeek] == 'unspecified':                
                    print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i, LowestPrice[i].name, dist, LowestPrice[i].prices[dayOfWeek], LowestPrice[i].delivery))
                elif len(LowestPrice[i].prices[dayOfWeek]) != 0:
                    print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i, LowestPrice[i].name, dist, LowestPrice[i].prices[dayOfWeek], LowestPrice[i].delivery))
        #checking for highest price
        if options[2] == 2:
            list(PricesOnly).sort(reverse = True)
            count = 0
            for i in list(PricesOnly):
                for val in range(len(listOfAllShops)):
                    if listOfAllShops[val].prices[dayOfWeek] == PricesOnly[i]:
                        HighestPrice.append(listOfAllShops[val])
                        count +=1
                        if count == 10:
                            break
            if len(HighestPrice) == 0:
                options = []
                return
            for i in range(len(HighestPrice)):
                dist = GD((str(HighestPrice[i].latitude),str(HighestPrice[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                if HighestPrice[i].price[dayOfWeek] == 'unspecified':                
                    print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,HighestPrice[i].name, dist, HighestPrice[i].prices[dayOfWeek], HighestPrice[i].delivery))
                elif len(HighestPrice[i].prices[dayOfWeek]) != 0:
                    print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,HighestPrice[i].name, dist, HighestPrice[i].prices[dayOfWeek], HighestPrice[i].delivery))

    #checking for prices and delivery day
    if options[2] and options[1] and options[0] == None:
        for loc in listOfAllShops:
            if loc.prices[dayOfWeek] != 'unspecified':
                PricesOnly.add(loc.prices[dayOfWeek])
        if len(list(PricesOnly)) == 0:
            options = []
            return
        #checking for recent delivery and low price
        if options[1] == 1 and options[2] == 1:
            list(PricesOnly).sort()
            count = 0
            for i in list(PricesOnly):
                for val in range(len(deliveryRecent)):
                    if deliveryRecent[val].prices[dayOfWeek] == PricesOnly[i]:
                        LowPriceRecentDeliver.append(deliveryRecent[val])
                        count +=1
                        if count == 10:
                            break
            if len(LowPriceRecentDeliver) == 0:
                options = []
                return
            for i in range(len(LowPriceRecentDeliver)):
                dist = GD((str(LowPriceRecentDeliver[i].latitude),str(LowPriceRecentDeliver[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                if LowPriceRecentDeliver[i].price[dayOfWeek] == 'unspecified':                
                    print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,LowPriceRecentDeliver[i].name, dist, LowPriceRecentDeliver[i].prices[dayOfWeek],
                    LowPriceRecentDeliver[i].delivery))
                elif len(LowPriceRecentDeliver[i].prices[dayOfWeek]) != 0:
                    print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,LowPriceRecentDeliver[i].name, dist, LowPriceRecentDeliver[i].prices[dayOfWeek], 
                    LowPriceRecentDeliver[i].delivery))
        #checking for recent delivery and high price   
        if options[1] == 1 and options[2] == 2:
            list(PricesOnly).sort(reverse = True)
            count = 0
            for i in list(PricesOnly):
                for val in range(len(deliveryRecent)):
                    if deliveryRecent[val].prices[dayOfWeek] == PricesOnly[i]:
                        HighPriceRecentDeliver.append(deliveryRecent[val])
                        count +=1
                        if count == 10:
                            break
            if len(HighPriceRecentDeliver) == 0:
                options = []
                return
            for i in range(len(HighPriceRecentDeliver)):
                dist = GD((str(HighPriceRecentDeliver[i].latitude),str(HighPriceRecentDeliver[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                if HighPriceRecentDeliver[i].price[dayOfWeek] == 'unspecified':                
                    print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,HighPriceRecentDeliver[i].name, dist, HighPriceRecentDeliver[i].prices[dayOfWeek],
                    HighPriceRecentDeliver[i].delivery))
                elif len(HighPriceRecentDeliver[i].prices[dayOfWeek]) != 0:
                    print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,HighPriceRecentDeliver[i].name, dist, HighPriceRecentDeliver[i].prices[dayOfWeek], 
                    HighPriceRecentDeliver[i].delivery))
        
        #checking for soon delivery and low price   
        if options[1] == 2 and options[2] == 1:
            list(PricesOnly).sort()
            count = 0
            for i in list(PricesOnly):
                for val in range(len(deliverySoon)):
                    if deliverySoon[val].prices[dayOfWeek] == PricesOnly[i]:
                        LowPriceSoonDeliver.append(deliverySoon[val])
                        count +=1
                        if count == 10:
                            break
            if len(LowPriceSoonDeliver) == 0:
                options = []
                return
            for i in range(len(LowPriceSoonDeliver)):
                dist = GD((str(LowPriceSoonDeliver[i].latitude),str(LowPriceSoonDeliver[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                if LowPriceSoonDeliver[i].price[dayOfWeek] == 'unspecified':                
                    print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,LowPriceSoonDeliver[i].name, dist, LowPriceSoonDeliver[i].prices[dayOfWeek],
                                                                                        LowPriceSoonDeliver[i].delivery))
                elif len(LowPriceSoonDeliver[i].prices[dayOfWeek]) != 0:
                    print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,LowPriceSoonDeliver[i].name, dist, LowPriceSoonDeliver[i].prices[dayOfWeek], 
                                                                                                LowPriceSoonDeliver[i].delivery))
        #checking for soon delivery and high price   
        if options[1] == 2 and options[2] == 2:
            list(PricesOnly).sort(reverse=True)
            count = 0
            for i in list(PricesOnly):
                for val in range(len(deliverySoon)):
                    if deliverySoon[val].prices[dayOfWeek] == PricesOnly[i]:
                        HighPriceSoonDeliver.append(deliverySoon[val])
                        count +=1
                        if count == 10:
                            break
            if len(HighPriceSoonDeliver) == 0:
                options = []
                return
            for i in range(len(HighPriceSoonDeliver)):
                dist = GD((str(HighPriceSoonDeliver[i].latitude),str(HighPriceSoonDeliver[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                if HighPriceSoonDeliver[i].price[dayOfWeek] == 'unspecified':                
                    print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,HighPriceSoonDeliver[i].name, dist, HighPriceSoonDeliver[i].prices[dayOfWeek],
                                                                                        HighPriceSoonDeliver[i].delivery))
                elif len(HighPriceSoonDeliver[i].prices[dayOfWeek]) != 0:
                    print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,HighPriceSoonDeliver[i].name, dist, HighPriceSoonDeliver[i].prices[dayOfWeek], 
                                                                                                HighPriceSoonDeliver[i].delivery))
        #checking for recent delivery and unspecified price   
        if options[1] == 1 and options[2] == 3:
            for loc in listOfAllShops:
                if loc.prices[dayOfWeek] == 'unspecified' and loc in deliveryRecent:
                    RecentUnspecified.append(loc)
            if len(RecentUnspecified) == 0:
                options = []
                return
            for i in range(len(RecentUnspecified)):
                dist = GD((str(RecentUnspecified[i].latitude),str(RecentUnspecified[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km               
                print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,RecentUnspecified[i].name, dist, RecentUnspecified[i].prices[dayOfWeek],
                RecentUnspecified[i].delivery))

        #checking for soon delivery and unspecified price   
        if options[1] == 2 and options[2] == 3:
            for loc in listOfAllShops:
                if loc.prices[dayOfWeek] == 'unspecified' and loc in deliverySoon:
                    SoonUnspecified.append(loc)
            if len(SoonUnspecified) == 0:
                options = []
                return
            for i in range(len(SoonUnspecified)):
                dist = GD((str(SoonUnspecified[i].latitude),str(SoonUnspecified[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km               
                print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,SoonUnspecified[i].name, dist, SoonUnspecified[i].prices[dayOfWeek],
                SoonUnspecified[i].delivery))

    #checking for delivery, distance and price
    if options[0] != None:
        if options[0]>0 and options[1] and options[2]: 
            #geting recent delivery in a distance       
            if options[1] == 1:
                for i in range(len(deliveryRecent)):
                    if deliveryRecent[i] in distanceCheck:
                        distdelRecent.append(deliveryRecent[i])
                if len(distdelRecent) == 0:
                    options = []
                    return
            #geting soon delivery in a distance 
            if options[1] == 2:
                for i in range(len(deliverySoon)):
                    if deliverySoon[i] in distanceCheck:
                        distdelSoon.append(deliverySoon[i])
                if len(distdelSoon) == 0:
                    options = []
                    return
            #geting unspecified prices for soon delivery in a distance
            if options[2] == 3 and options[1] == 2:
                for i in range(len(distdelSoon)):
                    if distdelSoon[i].prices[dayOfWeek] == 'unspecified':
                        distdelSoonUnspecified.append(distdelSoon[i])
                if len(distdelSoonUnspecified) == 0:
                    options = []
                    return
                for i in range(len(distdelSoonUnspecified)):
                    dist = GD((str(distdelSoonUnspecified[i].latitude),str(distdelSoonUnspecified[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km               
                    print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,distdelSoonUnspecified[i].name, dist, distdelSoonUnspecified[i].prices[dayOfWeek],
                    distdelSoonUnspecified[i].delivery))
            #geting unspecified prices for recent delivery in a distance
            if options[2] == 3 and options[1] == 1:
                for i in range(len(distdelRecent)):
                    if distdelRecent[i].prices[dayOfWeek] == 'unspecified':
                        distdelRecentUnspecified.append(distdelRecent[i])
                if len(distdelRecentUnspecified) == 0:
                    options = []
                    return
                for i in range(len(distdelRecentUnspecified)):
                    dist = GD((str(distdelRecentUnspecified[i].latitude),str(distdelRecentUnspecified[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km               
                    print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,distdelRecentUnspecified[i].name, dist, distdelRecentUnspecified[i].prices[dayOfWeek],
                    distdelRecentUnspecified[i].delivery))

            #Recent delivery and expensive price in a distance
            if options[2] == 2 and options[1] == 1:
                for loc in distdelRecent:
                    if loc.prices[dayOfWeek] != 'unspecified':
                        PricesOnly.add(loc.prices[dayOfWeek])
                if len(list(PricesOnly)) == 0:
                    options = []
                    return
                list(PricesOnly).sort(reverse = True)
                count = 0
                for i in range(len(PricesOnly)):
                    for val in range(distdelRecent):
                        if distdelRecent[val].prices[dayOfWeek] == PricesOnly[i]:
                            if not (distdelRecent[val] in distdelRecentExp):
                                distdelRecentExp.append(distdelRecent[val])
                                if (count==10 and i!=0) or (count>10 and i==1):
                                    break
                                count+=1
                if len(distdelRecentExp) == 0:
                    options = []
                    return
                for i in range(len(distdelRecentExp)):
                    dist = GD((str(distdelRecentExp[i].latitude),str(distdelRecentExp[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                    if distdelRecentExp[i].price[dayOfWeek] == 'unspecified':                
                        print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,distdelRecentExp[i].name, dist, distdelRecentExp[i].prices[dayOfWeek],
                        distdelRecentExp[i].delivery))
                    elif len(distdelRecentExp[i].prices[dayOfWeek]) != 0:
                        print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,distdelRecentExp[i].name, dist, distdelRecentExp[i].prices[dayOfWeek], 
                        distdelRecentExp[i].delivery))
            #Recent delivery and cheap price in a distance
            if options[2] == 1 and options[1] == 1:
                for loc in distdelRecent:
                    if loc.prices[dayOfWeek] != 'unspecified':
                        PricesOnly.add(loc.prices[dayOfWeek])
                if len(list(PricesOnly)) == 0:
                    options = []
                    return
                list(PricesOnly).sort(reverse = True)
                count = 0
                for i in range(len(PricesOnly)):
                    for val in range(len(distdelRecent)):
                        if distdelRecent[val].prices[dayOfWeek] == PricesOnly[i]:
                            if not (distdelRecent[val] in distdelRecentCheap):
                                distdelRecentCheap.append(distdelRecent[val])
                                if (count==10 and i!=0) or (count>10 and i==1):
                                    break
                                count+=1
                if len(distdelRecentCheap) == 0:
                    options = []
                    return
                for i in range(len(distdelRecentCheap)):
                    dist = GD((str(distdelRecentCheap[i].latitude),str(distdelRecentCheap[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                    if distdelRecentCheap[i].price[dayOfWeek] == 'unspecified':                
                        print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,distdelRecentCheap[i].name, dist, distdelRecentCheap[i].prices[dayOfWeek],
                        distdelRecentCheap[i].delivery))
                    elif len(distdelRecentCheap[i].prices[dayOfWeek]) != 0:
                        print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,distdelRecentCheap[i].name, dist, distdelRecentCheap[i].prices[dayOfWeek], 
                        distdelRecentCheap[i].delivery))
            #Soon delivery and expensive price in a distance
            if options[2] == 2 and options[1] == 2:
                for loc in distdelSoon:
                    if loc.prices[dayOfWeek] != 'unspecified':
                        PricesOnly.add(loc.prices[dayOfWeek])
                if len(list(PricesOnly)) == 0:
                    options = []
                    return
                list(PricesOnly).sort()
                count = 0
                if options[1] == 2:
                    for i in range(len(PricesOnly)):
                        for val in range(len(distdelSoon)):
                            if distdelSoon[val].prices[dayOfWeek] == PricesOnly[i]:
                                if not (distdelSoon[val] in distdelSoonExp):
                                    distdelSoonExp.append(distdelSoon[val])
                                    if (count==10 and i!=0) or (count>10 and i==1):
                                        break
                                    count+=1
                if len(distdelSoonExp) == 0:
                    options = []
                    return
                for i in range(len(distdelSoonExp)):
                    dist = GD((str(distdelSoonExp[i].latitude),str(distdelSoonExp[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                    if distdelSoonExp[i].price[dayOfWeek] == 'unspecified':                
                        print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,distdelSoonExp[i].name, dist, distdelSoonExp[i].prices[dayOfWeek],
                        distdelSoonExp[i].delivery))
                    elif len(distdelSoonExp[i].prices[dayOfWeek]) != 0:
                        print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i,distdelSoonExp[i].name, dist, distdelSoonExp[i].prices[dayOfWeek], 
                        distdelSoonExp[i].delivery))   
            #Soon delivery and cheap price in a distance
            if options[2] == 1 and options[1] == 2:
                for loc in distdelSoon:
                    if loc.prices[dayOfWeek] != 'unspecified':
                        PricesOnly.add(loc.prices[dayOfWeek])
                if len(list(PricesOnly)) == 0:
                    options = []
                    return
                list(PricesOnly).sort()
                count = 0
                if options[1] == 2:
                    for i in range(len(PricesOnly)):
                        for val in range(len(distdelSoon)):
                            if distdelSoon[val].prices[dayOfWeek] == PricesOnly[i]:
                                if not (distdelSoon[val] in distdelSoonCheap):
                                    distdelSoonCheap.append(distdelSoon[val])
                                    if (count==10 and i!=0) or (count>10 and i==1):
                                        break
                                    count+=1
                if len(distdelSoonCheap) == 0:
                    options = []
                    return
                for i in range(len(distdelSoonCheap)):
                    dist = GD((str(distdelSoonCheap[i].latitude),str(distdelSoonCheap[i].longitude)), (YourLocation.latitude, YourLocation.longitude)).km
                    if distdelSoonCheap[i].price[dayOfWeek] == 'unspecified':                
                        print("{} - {}: Distance: {} km, Price: {}, Delivery day: {}".format(i,distdelSoonCheap[i].name, dist, distdelSoonCheap[i].prices[dayOfWeek],
                        distdelSoonCheap[i].delivery))
                    elif len(distdelSoonCheap[i].prices[dayOfWeek]) != 0:
                        print("{} - {}: Distance: {} km, Price: {} per kg, Delivery day: {}".format(i, distdelSoonCheap[i].name, dist, distdelSoonCheap[i].prices[dayOfWeek], 
                        distdelSoonCheap[i].delivery))

def ChangeData(YourLocation):
    global addressList
    altered = []
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*len(", ".join(addressList)))
        print(", ".join(addressList))
        print("="*len(", ".join(addressList)))
        print("(0) Change the city/town")
        print("(1) Change the street")
        print("(2) Change the house number")
        print("(3) Return")
        choice = CheckInputForExit()
        os.system('cls' if os.name == 'nt' else 'clear')
        match choice:
            case 0:
                try:
                    print("You entered before:", YourLocation.data['address']['city'])
                    print("="*(len(YourLocation.data['address']['city'])//2), "Add a new city/village/town:", "="*(len(YourLocation.data['address']['city'])//2))
                except:
                    try:
                        print("You entered before:", YourLocation.data['address']['village'])
                        print("="*(len(YourLocation.data['address']['village'])//2), "Add a new city/village/town:", "="*(len(YourLocation.data['address']['village'])//2))
                    except:
                        print("You entered before:", YourLocation.data['address']['town'])
                        print("="*(len(YourLocation.data['address']['town'])//2), "Add a new city/village/town:", "="*(len(YourLocation.data['address']['town'])//2))
                city = input()
                addressList.remove(addressList[1])
                addressList.insert(1, city)
                altered.append("city/town")
            case 1:
                try:
                    print("You entered before:", YourLocation.data['address']['road'])
                    print("="*(len(YourLocation.data['address']['road'])//2), "Add a new street", "="*(len(YourLocation.data['address']['road'])//2))
                except:
                    print("You entered before:", YourLocation.data['address']['neighbourhood'])
                    print("="*(len(YourLocation.data['address']['neighbourhood'])//2), "Add a new street", "="*(len(YourLocation.data['address']['neighbourhood'])//2))
                street = input()
                addressList.remove(addressList[2])
                addressList.insert(2, street)
                altered.append("street")
            case 2:
                try:
                    print("You entered before:", addressList[3])
                    print("="*(len(addressList[3])//2), "Add a new house number:", "="*(len(addressList[3])//2))
                    addressList.remove(addressList[3])
                except:
                    print("Add the house number:")
                number = input()
                addressList.insert(3, number)
                altered.append("house number")
            case 3:
                address = ", ".join(addressList) 
                print(address)
                try:
                    location = geolocator.geocode(address, addressdetails=True)
                    YourLocation.data = location.raw
                    YourLocation.latitude = location.latitude
                    YourLocation.longitude = location.longitude
                    return YourLocation
                except:
                    print("There is no such location/Your internet connection is unstable")
                    print("=========================")
                    print("You altered before: ")
                    for change in altered:
                        print(change)
                    time.sleep(3)
                    altered.clear()
            case 'exit':
                exit() 
        
def AddShop(YourLocation):
    country = "Poland"
    city = None
    street = None
    number = None
    deliveryday = None
    name = None
    prices = {'Monday': 0, 'Tuesday': 0,'Wednesday': 0,'Thursday': 0,'Friday': 0, 'Saturday': 0,'Sunday': 0}
    addressShop.insert(0, country)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==================================")
        print("(0) Return")
        print("(1) Add the name of the shop")
        print("(2) Add the name of the city/town/village")
        print("(3) Add the name of the street")
        print("(4) Add the house number")
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
                    text = "Previous name of the city/town/village: " + city
                    prRed(text)
                    addressShop.remove(city)
                print("Add the name of the city/town/village:")
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
                    text = "Previous house number: " + number
                    prRed(text)
                    addressShop.remove(number)
                print("Add the house number: ")
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
            addressShop.clear()
        except:
            addressShop.clear()
            print("There is no such location/Your internet connection is unstable")
            time.sleep(4)
            return 0
        if deliveryday == None:
            deliveryday = "unspecified"
        YourShop = Shops(name, location.latitude, location.longitude, data, deliveryday, prices)
        for shop in listOfAllShops:
            if name == shop.name and YourShop == shop:
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
                delivery = "Thursday"
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
    prices['Monday'] = 0
    prices['Tuesday'] = 0
    prices['Wednesday'] = 0
    prices['Thursday'] = 0
    prices['Friday'] = 0
    prices['Saturday'] = 0
    prices['Sunday'] = 0
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
                    try:
                        print("({}) - {}: {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'], 
                        listOfAllShops[i].data['address']['road'], listOfAllShops[i].data['address']['house_number']))
                    except:
                        print("({}) - {}: {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'], 
                        listOfAllShops[i].data['address']['neighbourhood'], listOfAllShops[i].data['address']['house_number']))
                except:
                    try:
                        print("({}) - {}: {}, {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'],
                        listOfAllShops[i].data['address']['road']))
                    except:
                        print("({}) - {}: {}, {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'],
                        listOfAllShops[i].data['address']['neighbourhood']))  
            except:
                try:
                    try:
                        print("({}) - {}:  {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road'], 
                        listOfAllShops[i].data['address']['house_number']))
                    except:
                        print("({}) - {}:  {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['neighbourhood'], 
                        listOfAllShops[i].data['address']['house_number']))
                except:
                    try:
                        print("({}) - {}: {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road']))
                    except:
                        print("({}) - {}: {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['neighbourhood']))
        print("=========================================")
        if len(listOfAllShops) == 0:
            print("(0) Add a new shop to Your database")
            print("(1) Return")
        else:
            print("(0) Check for details of a shop")
            print("(1) Add a new shop to Your database")
            print("(2) Remove a shop from Your database")
            print("(3) Change data of the shop")
            print("(4) Return")
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
                            try:
                                print("({}) - {}: {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'], 
                                listOfAllShops[i].data['address']['road'], listOfAllShops[i].data['address']['house_number']))
                            except:
                                print("({}) - {}: {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'], 
                                listOfAllShops[i].data['address']['neighbourhood'], listOfAllShops[i].data['address']['house_number']))
                        except:
                            try:
                                print("({}) - {}: {}, {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'],
                                listOfAllShops[i].data['address']['road']))
                            except:
                                print("({}) - {}: {}, {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'],
                                listOfAllShops[i].data['address']['neighbourhood']))
                    except:
                        try:
                            try:
                                print("({}) - {}:  {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road'], 
                                listOfAllShops[i].data['address']['house_number']))
                            except:
                                print("({}) - {}:  {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['neighbourhood'], 
                                listOfAllShops[i].data['address']['house_number']))
                        except:
                            try:
                                print("({}) - {}: {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road']))
                            except:
                                print("({}) - {}: {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['neighbourhood']))
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
                os.system('cls' if os.name == 'nt' else 'clear')
                match choice:
                    case 0:
                        for i in range(len(listOfAllShops)):
                            try:
                                try:
                                    try:
                                        print("({}) - {}: {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'], 
                                        listOfAllShops[i].data['address']['road'], listOfAllShops[i].data['address']['house_number']))
                                    except:
                                        print("({}) - {}: {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'], 
                                        listOfAllShops[i].data['address']['neighbourhood'], listOfAllShops[i].data['address']['house_number']))
                                except:
                                    try:
                                        print("({}) - {}: {}, {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'],
                                        listOfAllShops[i].data['address']['road']))
                                    except:
                                        print("({}) - {}: {}, {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'],
                                        listOfAllShops[i].data['address']['neighbourhood']))
                            except:
                                try:
                                    try:
                                        print("({}) - {}:  {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road'], 
                                        listOfAllShops[i].data['address']['house_number']))
                                    except:
                                        print("({}) - {}:  {}, {}, {} {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['neighbourhood'], 
                                        listOfAllShops[i].data['address']['house_number']))
                                except:
                                    try:
                                        print("({}) - {}: {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road']))
                                    except:
                                        print("({}) - {}: {}, {}".format(i+1, listOfAllShops[i].name, listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['neighbourhood']))
                        ("(0) Return")
                        print("Enter an index of a shop to change its data:")
                        id = CheckInputInt()
                        if id == 0:
                            pass
                        else:
                            while 0>id> len(listOfAllShops):
                                print("Try again: ")
                                id = CheckInputInt()
                            listOfAllShops[id-1].ChangeShopData()
            case 4:
                break
            case 'exit':
                exit()

def RemoveShopFromDatabase():
    print("(0) Return")
    print("Enter an index of a shop to remove from Your database")
    for i in range(0,len(listOfAllShops)):
        try:
            try:
                try:
                    print("({}) - {}: ".format(i+1, listOfAllShops[i].name), listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'], 
                    listOfAllShops[i].data['address']['road'], listOfAllShops[i].data['address']['house_number'])
                except:
                    print("({}) - {}: ".format(i+1, listOfAllShops[i].name), listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'], 
                    listOfAllShops[i].data['address']['neighbourhood'], listOfAllShops[i].data['address']['house_number'])
            except:
                try:
                    print("({}) - {}: ".format(i+1, listOfAllShops[i].name), listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'],
                    listOfAllShops[i].data['address']['road'])
                except:
                    print("({}) - {}: ".format(i+1, listOfAllShops[i].name), listOfAllShops[i].data['address']['city'], listOfAllShops[i].data['address']['suburb'],
                    listOfAllShops[i].data['address']['neighbourhood'])
        except:
            try:
                try:
                    print("({}) - {}: ".format(i+1, listOfAllShops[i].name), listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road'], 
                    listOfAllShops[i].data['address']['house_number'])
                except:
                    print("({}) - {}: ".format(i+1, listOfAllShops[i].name), listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['neighbourhood'], 
                    listOfAllShops[i].data['address']['house_number'])
            except:
                try:
                    print("({}) - {}: ".format(i+1, listOfAllShops[i].name), listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['road'])
                except:
                    print("({}) - {}: ".format(i+1, listOfAllShops[i].name), listOfAllShops[i].data['address']['village'], listOfAllShops[i].data['address']['neighbourhood'])
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
                    try:
                        location = geolocator.geocode(address, addressdetails=True)                    
                        if location.raw['address']['suburb'] == addressChoice[-1]:
                            return addressChoice[-1]
                        else:
                            print("There is no such district")
                            time.sleep(2)
                            break
                    except:
                        print("Your internet connection is unstable")
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
        try:
            location1 = geolocator.geocode(address1, exactly_one =False)
            for loc in location1:
                newLocations.append(loc)
        except:
            pass
        try:
            location2 = geolocator.geocode(address2, exactly_one =False)
            for loc in location2:
                newLocations.append(loc)
        except:
            pass
        try:
            location3 = geolocator.geocode(address3, exactly_one =False)
            for loc in location3:
                newLocations.append(loc)
        except:
            pass
        try:
            location4 = geolocator.geocode(address4, exactly_one =False)
            for loc in location4:
                newLocations.append(loc)
        except:
            pass
        try:
            location5 = geolocator.geocode(address5, exactly_one =False)
            for loc in location5:
                newLocations.append(loc)
        except:
            pass
        try:
            location6 = geolocator.geocode(address6, exactly_one =False)
            for loc in location6:
                newLocations.append(loc)
        except:
            pass
        try:
            location7 = geolocator.geocode(address7, exactly_one =False)
            for loc in location7:
                newLocations.append(loc)
        except:
            pass
        try:
            location8 = geolocator.geocode(address8, exactly_one =False)
            for loc in location8:
                newLocations.append(loc)
        except:
            pass
        try:
            location9 = geolocator.geocode(address9, exactly_one =False)
            for loc in location9:
                newLocations.append(loc)
        except:
            pass
        try:
            location10 = geolocator.geocode(address10, exactly_one =False)
            for loc in location10:
                newLocations.append(loc)
        except:
            pass
        try:
            location11 = geolocator.geocode(address11, exactly_one =False)
            for loc in location11:
                newLocations.append(loc)
        except:
            pass
        try:
            location12 = geolocator.geocode(address12, exactly_one =False)
            for loc in location12:
                newLocations.append(loc)
        except:
            pass
        try:
            location13 = geolocator.geocode(address13, exactly_one =False)
            for loc in location13:
                newLocations.append(loc)
        except:
            pass
        try:
            location14 = geolocator.geocode(address14, exactly_one =False)
            for loc in location14:
                newLocations.append(loc)
        except:
            pass
        try:
            location15 = geolocator.geocode(address15, exactly_one =False)
            for loc in location15:
                newLocations.append(loc)
        except:
            pass
        try:
            location16 = geolocator.geocode(address16, exactly_one =False)
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
            self.OperateOnFoundLocations(closestDatabase, district, 1)
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
        self.OperateOnFoundLocations(closestDatabase, radius, 0)
    def OperateOnFoundLocations(self, closestDatabase, distance, string):
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
                print("(2) Remove a shop from database")
                print("(3) Return")
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
                    closestDatabase = self.AddFoundShop(closestDatabase, distance, string)
                case 2:
                    RemoveShopFromDatabase()
                case 3:
                    newLocations.clear()
                    break
                case 'exit':
                    exit()
    def AddFoundShop(self, closestDatabase, distance, string):
        latlong = []
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
        addressShop = []
        checkBox = [0,0,0,0]
        addressShop.insert(0, "Poland")
        latitude = newLocations[id-1].latitude
        longitude = newLocations[id-1].longitude
        latlong.append(str(latitude))
        latlong.append(str(longitude))
        location = geolocator.reverse(", ".join(latlong))
        data = location.raw
        name = None
        try:
            city = data['address']['city']
        except:
            city = data['address']['village']
        try:
            street = data['address']['road']
        except:
            street = data['address']['neighbourhood']
        try:
            number = data['address']['house_number']
        except:
            number = "unspecified"
        addressShop.insert(1, city)
        addressShop.insert(2, street)
        addressShop.insert(3, number)
        prices = {}
        deliveryday = None
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("(0) Return")
            print("(1) Add the name of the shop")
            print("(2) Add the name of the city/town")
            print("(3) Add the name of the street")
            print("(4) Add the house number")
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
                    return closestDatabase
                case 1: 
                    if name != None:
                        text = "Previous name of the shop: "+ name
                        prRed(text)                 
                    print("Add the name of the shop or use (0) previous:")
                    nameNew = input()                    
                    if nameNew != "0":
                        name = nameNew
                        checkBox[0] = 1
                        
                case 2:
                    text = "Previous/default name of the city/village: "+ city
                    prRed(text)
                    print("Add the name of the city/village or use (0) previous/default:")
                    cityNew = input()
                    checkBox[1] = 1
                    if cityNew != "0":
                        city = cityNew                        
                        addressShop[1] = city
                case 3:
                    text = "Previous/default name of the street: " + street
                    prRed(text)
                    print("Add the name of the street or use (0) previous/default:")
                    streetNew = input()
                    checkBox[2] = 1
                    if streetNew != "0":
                        street = streetNew                        
                        addressShop[2] = street
                case 4:
                    if number != "unspecified":
                        text = "Previous/default house number: " + number
                        prRed(text)
                        print("Add the house number or use (0) previous/default: ")
                        numberNew = input()
                    else:
                        print("Add the house number: ")
                        number = input()
                    checkBox[3] = 1
                    if numberNew != "0":
                        number = numberNew
                        addressShop[3] = number
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
                print("There is no such location/Your internet connection is unstable")
                time.sleep(4)
                return 0
            YourShop = Shops(name, location.latitude, location.longitude, data, deliveryday, prices)
            for shop in listOfAllShops:
                if (YourShop.name == shop.name and YourShop.latitude == shop.latitude and YourShop.latitude == shop.longitude and YourShop.data == shop.data and
                YourShop.deliveryday == shop.deliveryday and YourShop.prices == shop.prices):
                    print("You already have this shop in Your database")
                    print("(0) Return")
                    print("(1) Check details of the shop")
                    choice = CheckInputForExit()
                    match choice:
                        case 0:
                            return closestDatabase
                        case 1:
                            YourShop.DisplayDetailsOfShop(self)
                        case 'exit':
                            exit()
            time.sleep(3)
            listOfAllShops.append(YourShop)
            UploadData()
            if string:
                try:
                    if YourShop.data['address']['suburb'] == distance:
                        closestDatabase.append(YourShop)
                        return closestDatabase
                except:
                    return closestDatabase
            elif not string:
                far = GD((str(YourShop.latitude),str(YourShop.longitude)), (self.latitude,self.longitude)).km
                if far <= distance:
                    closestDatabase.append(YourShop)
                    return closestDatabase
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
        today = date.today()
        week = ['Monday','Tuesady', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        getDay = date.weekday(today)
        dayOfWeek = week[getDay]
        distance = GD((self.latitude, self.longitude), (YourLocation.latitude, YourLocation.longitude)).km
        print("Name: {} - currently {} km from You".format(self.name, "%.3f" % distance))
        try:
            try:
                try:
                    print("Address: ", self.data['address']['city'], self.data['address']['suburb'], 
                    self.data['address']['road'], self.data['address']['house_number'])
                except:
                    print("Address: ", self.data['address']['city'], self.data['address']['suburb'], 
                    self.data['address']['neighbourhood'], self.data['address']['house_number'])
            except:
                try:
                    print("Address: ", self.data['address']['city'], self.data['address']['suburb'], 
                    self.data['address']['road'])
                except:
                    print("Address: ", self.data['address']['city'], self.data['address']['suburb'], 
                    self.data['address']['neighbourhood'])
        except:
            try:
                try:
                    print("Address: ", self.data['address']['village'], self.data['address']['road'], self.data['address']['house_number'])
                except:
                    print("Address: ", self.data['address']['village'], self.data['address']['neighbourhood'], self.data['address']['house_number'])
            except:
                try:
                    print("Address: ", self.data['address']['village'], self.data['address']['road'])
                except:
                    print("Address: ", self.data['address']['village'], self.data['address']['neighbourhood'])
        print((len(self.delivery))//2*"="+"Prices"+(len(self.delivery))//2*"=")  #finish
        for key, value in self.prices.items():
            print(key, ":", value)
        print((len(self.delivery))//2*"="+"Prices"+(len(self.delivery))//2*"=")
        print("Price for today:", self.prices[dayOfWeek])
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
    def ChangeShopData(self):
        addressShop = []
        addressShop.insert(0, "Poland")
        global listOfAllShops
        listOfAllShops.remove(self)
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("(0) Return")
            print("(1) Change the name of the shop")
            print("(2) Change city/town where the shop is")
            print("(3) Change the street where the shop is")
            print("(4) Change the house number of where the shop is")
            print("(5) Change the day of the delivery of the shop")
            print("(6) Change the prices of products in the shop")
            print("(7) Apply changes and return")
            choice = CheckInputForExit()
            os.system('cls' if os.name == 'nt' else 'clear')
            match choice:
                case 0:
                    listOfAllShops.append(self)
                    break
                case 1:
                    print("(0) return and keep original name")
                    print("Previous name of the shop: ", self.name)
                    name = input()
                    if name != "0":
                        newname = name
                case 2:
                    print("(0) return and keep original city/town")
                    try:
                        print("Previous city/town of the shop: ", self.data['address']['city'])
                    except:
                        print("Previous city/town of the shop: ", self.data['address']['village'])
                    city = input()
                    if city != "0":
                        addressShop.insert(1, city)
                case 3:
                    print("(0) return and keep original street")
                    try:
                        print("Previous city/town of the shop: ", self.data['address']['road'])
                    except:
                        print("Previous city/town of the shop: ", self.data['address']['neighbourhood'])
                    street = input()
                    if street != "0":
                        addressShop.insert(2, street)
                case 4:
                    print("(0) return and keep original house number")
                    try:
                        print("Previous city/town of the shop: ", self.data['address']['house_number'])
                    except:
                        print("There was no house number entered before")
                    number = input()
                    if number != "0":
                        addressShop.insert(3, number)
                case 5:
                    newdelivery = AddDeliveryDay(self.delivery)
                case 6:
                    newprices = AddPrices(self.prices)
                case 7:
                    address = ", ".join(addressShop)
                    try:
                        location = geolocator.geocode(address, addressdetails=True)
                        self.name = newname
                        self.prices = newprices
                        self.delivery = newdelivery
                        self.latitude = location.latitude
                        self.longitude = location.longiutde
                        self.data = location.raw
                        addressShop.clear()
                        listOfAllShops.append(self)
                        UploadData()                  
                        print(self.name)
                        print(address)
                        print("Delivery day: ", self.delivery)
                        for key, value in self.prices.items():
                            print(key, ":", value)
                        time.sleep(2)
                    except:
                        print("There is no such location/Your internet connection is unstable")
                        print("=========================")
                        print(self.name)
                        print(address)
                        print("Delivery day: ", self.delivery)
                        for key, value in self.prices.items():
                            print(key, ":", value)
                        addressShop.clear()
                        time.sleep(2)
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