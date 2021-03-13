import requests
import json
from keys import access_token, username, ships, shiplist

base_url = 'https://api.spacetraders.io/'
headers = {'Authorization':access_token}
payload = {}

shipclasses = ['MK-I', 'MK-II', 'MK-III']

#Gets user data ie ships, credits, loans, etc
def userstatus():
    res = requests.get(f'{base_url}users/{username}', headers=headers)
    data = res.json()
    print(data['user'])

def systeminfo():
    res = requests.get(f"{base_url}game/systems", headers = headers)
    data = res.json()
    print(data)

def planet():
    res = requests.get(f"{base_url}game/locations/")

def createuser():
    username = input('What do you want your username to be? ')
    res = requests.get(f'{base_url}users/{username}/token')
    data = res.json()
    print(data['token'])

def loan():
    needloan = input('Do you want to take a loan? Y/N ')
    if needloan == "Y" or "y":
        res = requests.get(f'{base_url}game/loans', headers=headers)
        data = res.json()
        availableloans = []
        for loan in data['loans']:
            availableloans.append(loan['type'])
            for loan in resdata['loans']:
                print(f"{loan['type']} for {loan['amount']}. Loan term is {loan['termInDays']} day(s).")
            loantype = input('What kind of loan do you want? ').upper()
            if loantype in availableloans:
                payload['type'] = loantype
                loanres = requests.post(f'{base_url}users/{username}/loans', headers = headers, data = payload)
            else:
                print('That loan is not available.')
    else:
        print("Thank you for visiting the bank")
        

def shipmarket():
    shipclass = input(f"What ship class would you like to shop for? ({shipclasses}) ").upper()
    payload['class'] = shipclass
    print(payload)
    res = requests.get(f'{base_url}game/ships', headers = headers, data = payload)
    payload.pop('class', None)
    data = res.json()
    shipsforsale = []
    shiplocations = []
    for ship in data['ships']:
        shipsforsale.append(ship['type'])
        print(f"Ship {ship['type']}")
        print(f"Class: {ship['class']}")
        print(f"Max Cargo: {ship['maxCargo']}")
        print(f"Speed: {ship['speed']}")
        print(f"Armor: {ship['plating']}")
        print(f"Weapons: {ship['weapons']}")
        for location in ship['purchaseLocations']:
            shiplocations.append(location['location'])
            print(f"Planet: {location['location']}")
            print(f"Price: {location['price']}")
        print('\n')
    buyship = input(f"Which ship would you like to buy? {shipsforsale} ").upper()
    if buyship in shipsforsale:
        payload['type'] = buyship
    buylocation = input(f"Where would you like to buy the ship from? {shiplocations} ").upper()
    if buylocation in shiplocations:
        payload['location'] = buylocation
    shipres = requests.post(f"{base_url}users/{username}/ships", headers = headers, data = payload)
    print(shipres)

def buyfuel():
    shiptofuel = input(f"Which ship do you want to fuel up? {shiplist} ")
    fuelquantity = int(input("How much fuel would you like? "))
    payload['shipId'] = ships[shiptofuel]
    payload['good'] = 'FUEL'
    payload['quantity'] = fuelquantity
    res = requests.post(f"{base_url}users/{username}/purchase-orders", headers = headers, data = payload)
    data = res.json()
    print(data)

def buygoods():
    shipname = input(f'What ship do you want to travel in? {shiplist} ').upper()
    payload['shipId'] = ships[shipname]
    payload['good'] = input("Which item would you like to purchase? ").upper()
    payload['quantity'] = int(input("How many would you like? "))
    res = requests.post(f"{base_url}users/{username}/purchase-orders", headers = headers, data = payload)
    print(res)

def sellgoods():
    shipname = input(f'What ship do you want to travel in? {shiplist} ').upper()
    payload['shipId'] = ships[shipname]
    payload['good'] = input("Which item would you like to sell? ").upper()
    payload['quantity'] = int(input("How many would you like to sell? "))
    res = requests.post(f"{base_url}users/{username}/sell-orders", headers = headers, data = payload)
    print(res)
    data = res.json()
    print(data)

def market():
    #Get ship name to retrieve shipId to find ship location.
    shipname = input(f"Which ship do you want to find? {shiplist} ").upper()
    payload['shipId'] = ships[shipname]
    getship = requests.get(f"{base_url}users/{username}/ships", headers = headers, data = payload)
    data = getship.json()
    location = data['ships'][0]['location']
    res = requests.get(f"{base_url}game/locations/{location}/marketplace", headers = headers)
    data = res.json()
    market = data['planet']['marketplace']
    for i in range(len(market)):
        print(f"Item: {market[i]['symbol']}")
        print(f"Size: {market[i]['volumePerUnit']}")
        print(f"Price: {market[i]['pricePerUnit']}")
        print(f"Quantity Available: {market[i]['quantityAvailable']} \n")
    store = input("Are you shopping or selling goods? B/S").upper()
    if store == "B":
        buygoods()
    elif store == "S":
        sellgoods()
    else:
        print("Thank you for shopping")

def findplanet():
    payload['type'] = 'PLANET'
    res = requests.get(f'{base_url}game/systems/OE/locations', headers = headers, data = payload)
    data = res.json()
    print(data['locations'])
    travel = input('Do you want to travel? Y/N ').upper()
    if travel == "Y":
        flightplan()
    else:
        print("Thank you for searching the solar system.")

def flightplan():
    destination = input('Where do you want to go? ').upper()
    shipname = input(f'What ship do you want to travel in? {shiplist} ').upper()
    payload['shipId'] = ships[shipname]
    payload['destination'] = destination
    res = requests.post(f'{base_url}users/{username}/flight-plans', headers = headers, data = payload)
    data = res.json()
    print(data)

