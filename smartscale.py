import os
import csv
import cv2
import numpy as np
import pandas as pd
import pickle
import msvcrt
import tensorflow as tf
from keras.preprocessing import image
from tensorflow import keras


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
            input('Press any key to continue')



class PictureTaker:
    # Takes single picture which can be then used in PicturePredicter class
    # Crops the image and resizes to 128 and then saves to path given in constructor
    # Path is same for all so overwriting is inevitable, unless uuid() or so is added

    def __init__(self, picture_path, cv2_cam=0, picture_size=128):
        self.picture_path = picture_path
        self.picture_size = picture_size
        self.cv2_cam = cv2_cam
        #self.cap = cv2.VideoCapture(cv2_cam, cv2.CAP_DSHOW)
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 280)

    def takePicture(self):
        print(self.picture_path)
        self.cap = cv2.VideoCapture(self.cv2_cam, cv2.CAP_DSHOW) 
        ret, frame = self.cap.read() 
        frame = self.crop_square(frame, self.picture_size, cv2.INTER_AREA) 
        cv2.imwrite(self.picture_path, frame)
        self.cap.release() 

    def takePictureWithClass(self, classname, amount): 
        picture_path = os.path.join(self.picture_path, classname) 
        for i in range(amount): 
            self.takePicture() 
            #self.cap = cv2.VideoCapture(self.cv2_cam, cv2.CAP_DSHOW) 
            #ret, frame = self.cap.read() 
            #frame = self.crop_square(frame, self.picture_size, cv2.INTER_AREA) 
            #cv2.imwrite(self.picture_path, frame) self.cap.release() 
    def displayPicture(self): 
        # Displays videoimega until ESC is pressed 
        print("\nDisplaying camera, press ESC on cmd to close")
        self.cap = cv2.VideoCapture(self.cv2_cam, cv2.CAP_DSHOW) 
        while(self.cap.isOpened()): 
            ret, frame = self.cap.read() 
            if ret == True: 
                cv2.imshow('frame', frame) 
                if msvcrt.kbhit(): 
                    if ord(msvcrt.getch()) == 27: 
                        break 
                cv2.waitKey(25) 
            else: 
                break 
        self.cap.release()
        cv2.destroyAllWindows()

# interpolation=cv2.INTER_AREA)
    def crop_square(self, img, size, interpolation):
        h, w = img.shape[:2]
        min_size = np.amin([h,w])

        # Centralize and crop
        crop_img = img[int(h/2-min_size/2):int(h/2+min_size/2), int(w/2-min_size/2):int(w/2+min_size/2)]
        resized = cv2.resize(crop_img, (size, size), interpolation=interpolation)

        return resized


class PicturePredicter:
    # When model is trained, it is saved and classnames are written to txt file
    # Give model_path and class_names path as argument and predict picture against the model...
    # ... By calling predictPicture with image path

    def __init__(self, model_path, classnames_path, picture_path, picture_size=128):
        self.model_path = model_path 
        self.classnames_path = classnames_path 
        self.model = tf.keras.models.load_model(self.model_path)
        self.classnames = pickle.loads(open(classnames_path, "rb").read())
        self.probability_model = tf.keras.Sequential([self.model, tf.keras.layers.Softmax()])
        self.picture_path = picture_path
        self.picture_size = 128

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

