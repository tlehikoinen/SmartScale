import os
import csv
import cv2
import uuid
import time
import numpy as np
import pandas as pd
import pickle
import subprocess
from time import sleep
import modules.config as cf

class PriceHandler: 
    # We need prices for our predicted products, so this class can be used for generating csv file...
    # ...which contains information about name and price
    # Price data can be later read / manipulated with functions
    def __init__(self, path, classnames, header=["name", "price_kg"]):
        self.path = path
        self.header = header
        self.classNames = classnames
        self.checkForPriceList()
    def printClassnames(self):
        print(self.classNames)

    def updateClassnames(self, classnames):
        self.classNames = classnames

    def checkForPriceList(self):
        if not os.path.exists(self.path):
            self.initialisePriceList()
        
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
            #print(price) 
            return price
        except:
            print("Item doesn't exist")

    def menu(self):
        continueProgram = True

        while(continueProgram):
            selection = input("\nPRICE MENU\n1. View items and prices \n2. Set prices for every item\n3. Change item price\n4. Get item price\n5. Reset (initialize)\n6. Go back to main menu")
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
                 print(self.returnPrice(item))
            elif selection == '5':
                self.initialisePriceList()
            elif selection == '6':
                # Returning so user is not asked to press key to continue
                continueProgram = False
                return
            else:
                print("Wrong input")
            input('Press enter key to continue')



class PictureTaker:
    # Takes single picture which can be then used in PicturePredicter class
    # Crops the image and resizes to 128 and then saves to path given in constructor
    # Path is same for all so overwriting is inevitable, unless uuid() or so is added

    # Add imagefolder_path and ?
    def __init__(self, picture_path):
        self.picture_path = picture_path
        self.picture_size = cf.picture_size
        self.cv2_cam = cf.cv2_cam
        #self.cap = cv2.VideoCapture(cv2_cam, cv2.CAP_DSHOW)
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 280)
     
    def takePicture(self):
        if os.name == 'nt':
            self.cap = cv2.VideoCapture(self.cv2_cam, cv2.CAP_DSHOW) 
        else:
            self.cap = cv2.VideoCapture(self.cv2_cam)

        pictureTaken = False
        counter = 0
        while(not pictureTaken):
            ret, frame = self.cap.read()
            counter+=1
            if counter == 10:
                frame = self.crop_square(frame, self.picture_size, cv2.INTER_AREA)
                cv2.imwrite(self.picture_path, frame)
                self.cap.release()
                pictureTaken = True

    def displayAndTakePicture(self, destroy=True): 
        # Displays videoimage and takes picture on ESC press (enter for rasp)
        print("\nDisplaying camera, press ESC on cmd to close")
        if os.name == "nt":
            self.cap = cv2.VideoCapture(self.cv2_cam, cv2.CAP_DSHOW) 
        else:
            self.cap = cv2.VideoCapture(self.cv2_cam)
        while(self.cap.isOpened()): 
            ret, frame = self.cap.read() 
            if ret == True: 
                cv2.imshow('frame', frame) 
                if self.checkForKeyPress():
                    frame = self.crop_square(frame, self.picture_size, cv2.INTER_AREA) 
                    cv2.imwrite(self.picture_path, frame)
                    break
                cv2.waitKey(25) 
            else: 
                break 
                #ret, frame = self.cap.read() 
        
        self.cap.release()
        if destroy == True:
            cv2.destroyAllWindows()

 
    def displayPicture(self, destroy=True): 
        # Displays videoimega until ESC is pressed 
        print("\nDisplaying camera, press ESC on cmd to close")
        if os.name == "nt":
            self.cap = cv2.VideoCapture(self.cv2_cam, cv2.CAP_DSHOW) 
        else:
            self.cap = cv2.VideoCapture(self.cv2_cam)
        while(self.cap.isOpened()): 
            ret, frame = self.cap.read() 
            if ret == True: 
                cv2.imshow('frame', frame) 
                if self.checkForKeyPress():
                    break
                cv2.waitKey(25) 
            else: 
                break 
        
        self.cap.release()
        if destroy == True:
            cv2.destroyAllWindows()

    def heardEnter(self):
        import select
        import sys
        i,o,e = select.select([sys.stdin],[],[],0.0001)
        for s in i:
            if s == sys.stdin:
                input = sys.stdin.readline()
                return True
        return False

    def checkForKeyPress(self):
        # Returns true if esc (win) or enter (rasp) is pressed
        if os.name == 'nt':
            import msvcrt
            if msvcrt.kbhit():
                if ord(msvcrt.getch()) == 27:
                    return True
        else:
            import sys
            import select
            i,o,e = select.select([sys.stdin],[],[],0.0001)
            for s in i:
                if s == sys.stdin:
                    input = sys.stdin.readline()
                    return True
        return False

    def crop_square(self, img, size, interpolation):
        h, w = img.shape[:2]
        min_size = np.amin([h,w])

        # Centralize and crop
        crop_img = img[int(h/2-min_size/2):int(h/2+min_size/2), int(w/2-min_size/2):int(w/2+min_size/2)]
        resized = cv2.resize(crop_img, (size, size), interpolation=interpolation)

        return resized

class PictureTakerWithClass(PictureTaker):
    # Before model is trained we must be able to take pictures to a folder named after a classname
    # This is a child class that inherits PictureTaker, and both are constructed with folder path
    # Before taking picture, parent classes picture_path is changed by address randomiser which ...
    # combines imagefolder_path and random address with .jpg extension
   
    def __init__(self, root_image_path, imagefolder_path, testimagefolder_path, no_model=True):
        PictureTaker.__init__(self,imagefolder_path)
        self.imagefolder_root_path = root_image_path
        self.testimagefolder_path = testimagefolder_path
        # root path remembers, class path mutates
        self.imagefolder_root_class_path = imagefolder_path 
        self.imagefolder_class_path = imagefolder_path
        self.no_model = no_model
        if not os.path.exists(root_image_path):
            os.makedirs(root_image_path)

        if not os.path.exists(self.imagefolder_root_class_path):
            self.initialisePictures()

    def randomisePictureDestinationAddress(self, root_path):
        #image_path = os.path.join(self.imagefolder_class_path, str(uuid.uuid1()) + '.jpg')
        image_path = os.path.join(root_path, str(uuid.uuid1()) + '.jpg')
        self.picture_path = image_path

    def printPaths(self):
        print("Imagefolder root path: " + self.imagefolder_root_path)
        print("Imagefolder root class path: " + self.imagefolder_root_class_path)
        print("Imagefolder class path:" + self.imagefolder_class_path)

    def takePictureRandomAddress(self, path):
        self.randomisePictureDestinationAddress(path)
        self.displayAndTakePicture(False)
        #self.takePicture()
            
    def askUserAndTakePicturesWithClass(self):
        classname = input('For which class you want to take pictures ')
        amount = input('How many pictures you want to take ')
        self.takePicturesWithClass(classname, amount)

    def initialisePictures(self):
    # Training pictures and test pictures are located in separate folders
    # Training pictures are taken first
    # Makes sure that picture to be predicted has folder to be saved to
        if not os.path.exists(self.imagefolder_root_class_path):
            print("Path for pictures was not found, if you don't have trained model, you should take pictures")  
            if input ('Take pictures or continue without? Y/N ') == 'Y':
                #os.makedirs(self.imagefolder_root_path)
                mode_train = True
            else:
                return
            while(mode_train):
                self.askUserAndTakePicturesWithClass()
                if input('Continue taking pictures? Y/N ') != 'Y':
                    mode_train = False

            while(not mode_train):
                print('Taking testing pictures... ')
                classname = input("For which class you want to take testing pictures? ")
                amount = input("How many testing pictures you want to take? ")
                self.takeTrainingPicturesWithClass(classname, amount)

                if input('Continue taking training pictures? Y/N ') == 'N':
                    return

    
    def takePicturesWithClass(self, classname, amount):
        self.imagefolder_class_path = os.path.join(self.imagefolder_root_class_path, classname)
        if not os.path.exists(self.imagefolder_class_path):
            os.makedirs(self.imagefolder_class_path)
        print('\nTaking pictures for class: ' + classname + '\nFolder: ' + self.imagefolder_class_path)
        for i in range(int(amount)):
            #self.displayPicture(False)
            print("taking picture number " + str(i+1))
            self.takePictureRandomAddress(self.imagefolder_class_path)
            if i == int(amount) - 1:
                cv2.destroyAllWindows()

    def printInfoAboutImages(self):
        # Prints console how many pictures each imagefolder have
        try:
            directories = os.listdir(self.imagefolder_root_class_path)
        except:
            print("Classpictures weren't found")
            return
        file_counts = []
        for index, item in enumerate(directories):
            file_counts.append({'classname': item, 'count': len(os.listdir(os.path.join(self.imagefolder_root_class_path, item)))})
        
        try:
            training_directories = os.listdir(self.testimagefolder_path)
        except:
            print("Testing pictures weren't found")
            return

        training_file_counts = []
        for index, item in enumerate(training_directories):
            training_file_counts.append({'classname': item, 'count': len(os.listdir(os.path.join(self.testimagefolder_path, item)))})

        print("\nClassname Count:\n")
        for item in file_counts:
            print(str(item.get('classname')) + " " + str(item.get('count')))

        print("\nTraining class count:\n")
        for item in training_file_counts:
            print(str(item.get('classname')) + " " + str(item.get('count')))
        # Print image counts and are counts even
        
    def takeTrainingPicturesWithClass(self, classname, amount):
            self.imagefolder_class_path = os.path.join(self.testimagefolder_path, classname)
            if not os.path.exists(self.imagefolder_class_path):
                os.makedirs(self.imagefolder_class_path)
            print('\nTaking pictures for class: ' + classname + '\nFolder: ' + self.testimagefolder_path)
            for i in range(int(amount)):
                #self.displayPicture(False)
                print("taking picture number " + str(i+1))
                self.takePictureRandomAddress(self.imagefolder_class_path)
                if i == int(amount) - 1:
                    cv2.destroyAllWindows()


    def movePictures():
        # Maybe images need to be moved
        pass
    def printinfo():
        # Print info like classnames, file counts, are folders missing pictures etc..
        pass

    def menu(self):
        continueProgram = True

        while(continueProgram):
            selection = input("\nTRAINING MENU\n1. Take pictures with class\n2. Take testing pictures \n3. Get current paths\n4. Print info\n5. Go back to main menu")
            if selection == '1':
                classname = input("For which class you want to take pictures? ")
                amount = input("How many pictures you want to take? ")
                self.takePicturesWithClass(classname, amount)
            elif selection == '2':
                classname = input("For which class you want to take testing pictures? ")
                amount = input("How many testing pictures you want to take? ")
                self.takeTrainingPicturesWithClass(classname, amount)
            elif selection == '3':
                self.printPaths()
            elif selection == '4':
                self.printInfoAboutImages()
            elif selection == '5':
                continueProgram = False
                if self.no_model:
                    exit()
                return

            elif selection == 'train':
                if input("Retrain model? (requires restart) Y/N") == 'Y':
                    subprocess.call("python trainmodel.py", shell=True)
                    input("Model was retrained, exit with enter...")
                    exit()
            else:
                print("Wrong input")
            input('Press enter key to continue')

class Numpad:
    def waitForUserInput(self):
        return input("Up or down U/D")

class LcdHandler():
    #Inherits CharLCD, probably needs to be used in own program to avoid collisions with windows system 
    #def __init__(self):
    #    CharLCD.__init__(self, pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21,22,23,24],
    #            numbering_mode=GPIO.board)
        
    def printInfo(self, info):
        print("LCD HANDLER " + info + " LCD HANDLER")

    def writeString(self, string):
        #self.write_string(string)
        #sleep(2)
        #self.clear()
        print(string)

    def stop(self):
        self.clear()
        GPIO.cleanup()

class Menu(Numpad, LcdHandler):
    # Protyping menu system for 16*2 lcd screen with keypad
    # Construct different menus, keep hold of current,
    # return state, move to next, move to previous etc..
    # Inherits Numpad which asks for user input 
    def __init__(self, menuItems):
        self.menuItems = menuItems
        self.menuItems.append('Exit')
        self.currentState = State(0, menuItems[0])

    def printMenuItems(self):
        for item in self.menuItems:
            print(item)
    
    def printCurrentState(self):
        print("Item: " + self.currentState.item + " index: " + str(self.currentState.index))

    def getCurrentState(self):
        return self.currentState

    def moveToPreviousState(self):
        if self.currentState.index == 0:
            self.currentState.index = len(self.menuItems)-1
            self.currentState.item = self.menuItems[self.currentState.index]
        #elif self.currentState.index == len(self.menuItems):
        #    self.currentState.index = len(self.menuItems)-1
        #    self.currentState.item = self.menuItems[self.currentState.index]
        else:
            self.currentState.index = self.currentState.index - 1
            self.currentState.item = self.menuItems[self.currentState.index]

    def moveToNextState(self):
        if self.currentState.index == len(self.menuItems) -1:
            self.currentState.index = 0 
            self.currentState.item = self.menuItems[self.currentState.index]
        #elif self.currentState.index == len(self.menuItems):
        #    return
        else:
            self.currentState.index = self.currentState.index + 1
            self.currentState.item = self.menuItems[self.currentState.index]
    
    def moveUpOrDown(self, direction):
        if direction == 'U':
            self.moveToNextState()
        elif direction == 'D':
            self.moveToPreviousState()

    def display(self):
        # This will eventually display row on lcd screeen
        self.currentState.index = 0
        self.currentState.item = self.menuItems[self.currentState.index]
        self.printCurrentState()
        selection = self.waitForUserInput()
        while (selection != 'E'):
            self.moveUpOrDown(selection)
            self.printCurrentState()
            self.printInfo(self.getCurrentState().item)
            selection = self.waitForUserInput()
        print('Leaving menu with index ' + str(self.getCurrentState().index))
        return self.getCurrentState().index 

    def displayLcd(self):
        self.currentState.index = 0
        self.currentState.item = self.menuItems[self.currentState.index]
        self.printCurrentState()
        selection = self.waitForUserInput()
        while (selection != 'E'):
            self.moveUpOrDown(selection)
            self.printCurrentState()
            self.printInfo(self.getCurrentState().item)
            selection = self.waitForUserInput()
        print('Leaving menu with index ' + str(self.getCurrentState().index))
        return self.getCurrentState().index 


class State:
    def __init__(self, index, menuItem):
        self.index = index
        self.item = menuItem

class Datasaver:
    def __init__(self, path, header=['Date', 'Product','Weight','PricePerKilo','TotalPrice']):
        self.path=path
        self.header=header
        self.checkForExisting()
 
    def checkForExisting(self):
        if not os.path.isfile(self.path):
            with open (self.path, 'w', newline='') as csvfile:
                pricewriter = csv.writer(csvfile, delimiter=',')
                pricewriter.writerow(self.header)
        else:
            print("file exists")
            #pass
 
    def saveData(self,product,priceperkilo,weight):
        from datetime import date
        today = date.today()
        weightInKg = weight/1000
        totalprice = round(priceperkilo * weightInKg, 2)
        #print('The TotalPrice is: ',totalprice)
        #print("Today's date is :", today)

        arrayOfItems=[str(today), str(product), str(weightInKg), str(priceperkilo), str(totalprice)]
        with open(self.path, 'a', newline='') as f:
          writer = csv.writer(f, delimiter=',')
          writer.writerow(arrayOfItems)
 
 
if __name__ == "__main__":
    main()
