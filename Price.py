import os
import csv
import pandas as pd

class PriceHandler: 
    # We need prices for our predicted products, so this class can be used for generating csv file...
    # ...which contains information about name and price
    # Price data can be later read / manipulated with functions
    def __init__(self, path, header, classnames):
        self.path = path
        self.header = header
        self.classNames = classnames

    def printClassNames(self):
        print(self.classNames)

    # Creates/overrides existing price file with classnames and price set to zero...
    # ... User is asked for confirmation if file exists
    def initialisePriceList(self):
        if os.path.exists(self.path):
            if not input("Price file already exists, override all data? Y/N") == "Y":
                print("Quitting...")
                return
            else:
                print("Overriding the data...")

        with open (self.path, 'w', newline='') as csvfile:
            pricewriter = csv.writer(csvfile, delimiter=',')
            pricewriter.writerow(self.header)
            for item in self.classNames:
                pricewriter.writerow([item, 0])
    
    # Change items price
    def changePrice(self, classname, newPrice):
        df = pd.read_csv(self.path)
        df.loc[df['name']==classname, "price_kg"] = newPrice
        df.to_csv(self.path, index=False)
    
    # Prints all items and prices
    def printPrices(self):
        if not os.path.exists(self.path):
            print("File doesn't exist yet, initialise first")
        else:
            print("Printing prices\n")
            with open(self.path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                print('Name Price')
                for row in reader:
                    print(row['name'] + ' ' + row['price_kg'])

    # For every item user is asked to give price
    def setPrices(self):
        print("Asking prices")
        df = pd.read_csv(self.path)
        for name in df['name']:
            price = input('Give price for ' + name + ': ')
            df.loc[df['name']==name, "price_kg"] = price
        df.to_csv(self.path, index=False)

    # Return price for classname
    def returnPrice(self, classname):
        df = pd.read_csv(self.path)
        try:
            price = df.loc[df["name"]==classname, "price_kg"].values[0]
            print(price) 
            return price
        except:
            print("Item doesn't exist")

    def menu(self):
        continueProgram = True

        while(continueProgram):
            selection = input("\nWhat you want to do?\n1. View items and prices \n2. Set prices for every item\n3. Change item price\n4. Get item price\n5. Reset (initialize)\n6. Quit\n")
            if selection == '1':
                self.printPrices()
            elif selection == '2':
                if input("You really want to set prices for every item? Y/N") == "Y":
                    self.setPrices()
            elif selection == '3':
                self.printPrices()
                item = input("Which items price you want to change? ")
                price = input("Give a new price ")
                self.changePrice(item, price)
            elif selection == '4':
                 item = input("Which items price you want to get? ")
                 self.returnPrice(item)
            elif selection == '5':
                self.initialisePriceList()
            elif selection == '6':
                continueProgram = False
            else:
                print("Wrong input")
            input('Press any key to continue')
