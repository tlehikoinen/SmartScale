import os
import csv
import cv2
import uuid
import time
import numpy as np
import pandas as pd
import pickle
#import msvcrt
#import select
import tensorflow as tf
from keras.preprocessing import image
from tensorflow import keras
import subprocess

class PriceHandler: 
    # We need prices for our predicted products, so this class can be used for generating csv file...
    # ...which contains information about name and price
    # Price data can be later read / manipulated with functions
    def __init__(self, path, classnames, header=["name", "price_kg"]):
        self.path = path
        self.header = header
        self.classNames = classnames

    def printClassnames(self):
        print(self.classNames)

    def updateClassnames(self, classnames):
        self.classNames = classnames

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
    def __init__(self, picture_path, cv2_cam=0, picture_size=128):
        self.picture_path = picture_path
        self.picture_size = picture_size
        self.cv2_cam = cv2_cam
        #self.cap = cv2.VideoCapture(cv2_cam, cv2.CAP_DSHOW)
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 280)
     
    def takePicture(self):
        if os.name == 'nt':
            self.cap = cv2.VideoCapture(self.cv2_cam, cv2.CAP_DSHOW) 
        elif os.name == 'unix':
            self.cap = cv2.VideoCapture(self.cv2_cam)
           
        print(self.picture_path)
        ret, frame = self.cap.read() 
        frame = self.crop_square(frame, self.picture_size, cv2.INTER_AREA) 
        cv2.imwrite(self.picture_path, frame)
        self.cap.release() 

    def displayPicture(self, destroy=True): 
        # Displays videoimega until ESC is pressed 
        print("\nDisplaying camera, press ESC on cmd to close")
        self.cap = cv2.VideoCapture(self.cv2_cam, cv2.CAP_DSHOW) 
        while(self.cap.isOpened()): 
            ret, frame = self.cap.read() 
            if ret == True: 
                cv2.imshow('frame', frame) 
                if self.checkForKeyPress() == True:
                    break 
                cv2.waitKey(25) 
            else: 
                break 
        
        self.cap.release()
        if destroy == True:
            cv2.destroyAllWindows()

    def checkForKeyPress(self):
        if os.name == 'nt':
            import msvcrt
            if msvcrt.kbhit():
                if ord(msvcrt.getch()) == 27:
                    return True
        elif os.name == 'unix':
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
   
    def __init__(self, root_image_path, imagefolder_path, testimagefolder_path):
        PictureTaker.__init__(self,imagefolder_path)
        self.imagefolder_root_path = root_image_path
        self.testimagefolder_path = testimagefolder_path
        self.imagefolder_class_path = imagefolder_path 
        if not os.path.exists(imagefolder_path):
            self.initialisePictures()

    def randomisePictureDestinationAddress(self, root_path):
        image_path = os.path.join(self.imagefolder_class_path, str(uuid.uuid1()) + '.jpg')
        self.picture_path = image_path

    def printPaths(self):
        print("Imagefolder root path: " + self.imagefolder_root_path)
        print("Imagefolder class path: " + self.imagefolder_class_path)

    def takePictureRandomAddress(self, path):
        self.randomisePictureDestinationAddress(path)
        self.takePicture()
            
    def askUserAndTakePicturesWithClass(self):
        classname = input('For which class you want to take pictures ')
        amount = input('How many pictures you want to take ')
        self.takePicturesWithClass(classname, amount)

    def takeTrainingPicture(self):
        if not os.path.exists(self.testimagefolder_path):
            os.makedirs(self.testimagefolder_path)
        self.displayPicture(True)
        self.takePictureRandomAddress(self.testimagefolder_path)

    def initialisePictures(self):
        # Training pictures and test pictures are located in separate folders
        # Training pictures are taken first

        # Makes sure that picture to be predicted has folder to be saved to
        if not os.path.exists(self.imagefolder_root_path):
            os.makedirs(self.imagefolder_root_path)
        print("Path for pictures was not found, if you don't have trained model, you should take pictures")  
        if input ('Take pictures or continue without? Y/N ') == 'Y':
            mode_train = True
        else:
            return
        while(mode_train):
            self.askUserAndTakePicturesWithClass()
            if input('Continue taking pictures? Y/N ') != 'Y':
                mode_train = False

        while(not mode_train):
            print('Taking training pictures... ')
            self.takeTrainingPicture()
            if input('Continue taking training pictures? Y/N ') == 'N':
                return

    
    def takePicturesWithClass(self, classname, amount):
        self.imagefolder_class_path = os.path.join(self.imagefolder_class_path, classname)
        if not os.path.exists(self.imagefolder_class_path):
            os.makedirs(self.imagefolder_class_path)
        print('\nTaking pictures for class: ' + classname + '\nFolder: ' + self.imagefolder_class_path)
        for i in range(int(amount)):
            self.displayPicture(False)
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
            selection = input("\nTRAINING MENU\n1. Take pictures with class \n2. Get current paths\n3. Go back to main menu")
            if selection == '1':
                classname = input("For which class you want to take pictures? ")
                amount = input("How many pictures you want to take? ")
                self.takePicturesWithClass(classname, amount)
            elif selection == '2':
                self.printPaths()
            elif selection == '3':
                continueProgram = False
                return
            elif selection == 'train':
                if input("Retrain model? (requires restart) Y/N") == 'Y':
                    subprocess.call("trainmodel.py", shell=True)
                    input("Model was retrained, exit with enter...")
                    exit()
            else:
                print("Wrong input")
            input('Press enter key to continue')


class PicturePredicter:
    # When model is trained, it is saved and classnames are written to txt file
    # Give model_path and class_names path as argument and predict picture against the model...
    # ... By calling predictPicture with image path

    def __init__(self, model_path, classnames_path, picture_path, picture_size=128):
        self.model_path = model_path 
        self.classnames_path = classnames_path 
        self.picture_path = picture_path
        self.picture_size = 128
        if not os.path.exists(self.model_path):
            self.modelNotFound()
        self.classnames = pickle.loads(open(classnames_path, "rb").read())
        self.model = tf.keras.models.load_model(self.model_path)
        self.probability_model = tf.keras.Sequential([self.model, tf.keras.layers.Softmax()])

    def modelNotFound(self):
        input("Trained model not found, exit with enter and train it...")
        exit()
         
    def getClassnames(self):
        return self.classnames

    def returnPrediction(self):
        picture = image.load_img(self.picture_path, (self.picture_size, self.picture_size))
        picture = image.img_to_array(picture)
        picture = np.expand_dims(picture,axis=0)
        results = self.probability_model.predict(picture)
        class_number = np.argmax(results)
        class_probability = str(round((np.amax(results)*100), 2))
        print('GUESSES ' + str(self.classnames[class_number]) + ' PROBABILITY = ' + str(class_probability) + '%')
        return self.classnames[class_number]

    def returnFullPredictions(self):
        picture = image.load_img(self.picture_path, (self.picture_size, self.picture_size))
        picture = image.img_to_array(picture)
        picture = np.expand_dims(picture,axis=0)
        results = self.probability_model.predict(picture)
        class_number = np.argmax(results)
        class_probability = str(round((np.amax(results)*100), 2))
        print('GUESSES ' + str(self.classnames[class_number]) + ' PROBABILITY = ' + str(class_probability) + '%')
        flattened_result = np.array(results)
        flattened_result = flattened_result.flatten()
        for count, result in enumerate(flattened_result):
            print('Object name = ' + self.classnames[count] + ' Probability = ' + str(round((result*100), 2)))

class Numpad:
    def waitForUserInput(self):
        return input("Up or down U/D")

class Menu(Numpad):
    # Protyping menu system for 16*2 lcd screen with keypad
    # Construct different menus, keep hold of current,
    # return state, move to next, move to previous etc..
    # Inherits Numpad which asks for user input 
    def __init__(self, menuItems):
        self.menuItems = menuItems
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
            return
        elif self.currentState.index == len(self.menuItems):
            self.currentState.index = len(self.menuItems)-1
            self.currentState.item = self.menuItems[self.currentState.index]
        else:
            self.currentState.index = self.currentState.index - 1
            self.currentState.item = self.menuItems[self.currentState.index]

    def moveToNextState(self):
        if self.currentState.index == len(self.menuItems) -1:
            self.currentState.index +=1 
            self.currentState.item = 'Exit'
        elif self.currentState.index == len(self.menuItems):
            return
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
        self.printCurrentState()
        selection = self.waitForUserInput()
        while (selection != 'E'):
            self.moveUpOrDown(selection)
            self.printCurrentState()
            selection = self.waitForUserInput()
        print('Leaving menu with index ' + str(self.getCurrentState().index))
        return self.getCurrentState().index 
class State:
    def __init__(self, index, menuItem):
        self.index = index
        self.item = menuItem




