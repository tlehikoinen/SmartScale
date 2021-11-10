import os
from modules.smartscale import PictureTaker, PictureTakerWithClass, PriceHandler, Menu, Datasaver
from modules.litepredicter import PicturePredicterLite
from modules.raspberry import LcdHandler
import modules.config as cf
from modules.hx711py import HX711
from time import sleep

def main():

    model_path = cf.lite_model_path
    classnames_path = cf.classnames_path
    testpicture_path = cf.testpicture_path 
    images_folder = cf.images_folder 
    root_image_path = cf.root_image_path
    prices_path = cf.prices_path
    saved_data_path = cf.saved_data_path

    # If model doesn't exists, user can only access menu from which pictures can be taken with classnames
    modelExists = model_paths_exists(model_path, classnames_path)
    picturetaker = PictureTaker(testpicture_path)
    hx = HX711(29, 31)

    if modelExists:
        predicter = PicturePredicterLite(model_path, classnames_path, testpicture_path)
        pricehandler = PriceHandler(prices_path, predicter.getClassnames())
        lcd = LcdHandler()
        hx_init(hx,lcd, 1010)
        datasaver = Datasaver(saved_data_path)
    else:
        print("Model was not found")
        exit()

    continueProgram = True

    while(continueProgram):
        selection = input("\nPICTURE MENU\n1. Take picture and print data\n2. Run the scale program\n3. Display camera\n4. Open price menu\n5. Exit")
        if selection == '1':
            doFullPrediction(picturetaker, predicter,lcd, pricehandler, hx)
        if selection == '2':
            scaleProgram(picturetaker, predicter, lcd, pricehandler, hx, datasaver)
        elif selection == '3':
            picturetaker.displayPicture()
        elif selection == '4':
            pricehandler.menu()
        elif selection == '5':
            # Returning so user is not asked to press key to continue
            continueProgram = False
            lcd.stop()
            return
        else:
            print("Wrong input, try again")
        input("\nPress enter key to continue\n")

def doFullPrediction(picturetaker, predicter, lcd, pricehandler, hx):
    weight = hx_readvalue(hx)
    picturetaker.takePicture()
    guess = predicter.returnPrediction()
    price = pricehandler.returnPrice(guess)
    print("Product: " + guess + " Price: " + str(price))
    #weight = hx_readvalue(hx)
    lcd.writePrediction(guess, price, weight)

def doFullPredictionWithWeight(picturetaker, predicter, lcd, pricehandler, weight, datasaver):
    picturetaker.takePicture()
    guess = predicter.returnPrediction()
    price = pricehandler.returnPrice(guess)
    print("Product: " + guess + " Price: " + str(price))
    lcd.writePrediction(guess, price, weight)
    datasaver.saveData(guess, price, weight)

def scaleProgram(picturetaker, predicter, lcd, pricehandler, hx, datasaver):
    writeCount = 0
    print("Read values")
    while(True):
        if writeCount == 0:
            lcd.write_string("Place item")
            writeCount+=1

        print("***** Waiting for item on scale*****")
        value = hx_readvalue(hx)
        if value > 5:
            checkForFinalWeight(picturetaker, predicter, lcd, pricehandler, hx, value, datasaver)
            writeCount = 0
            lcd.clear()

        if picturetaker.checkForKeyPress():
            lcd.clear()
            return

def checkForFinalWeight(picturetaker, predicter, lcd, pricehandler, hx, value, datasaver):
    prev_val = round(value)
    count = 0
    print("*****Check for weight match *****")
    while(True):
        new_val = round(hx_readvalue(hx))
        # Return if item is removed from scale 
        if new_val < 5:
            return
        count = count + 1 
        if prev_val == new_val:
            doFullPredictionWithWeight(picturetaker, predicter, lcd, pricehandler, new_val, datasaver)
            print("same value " + str(count))
            waitForEmptyScale(hx)
            return
        else:
            prev_val = new_val

def waitForEmptyScale(hx):
    print("***** WAITING FOR EMPTY SCALE *****")
    while(True):
        if hx_readvalue(hx) < 5:
            return
    
def hx_init(hx, lcd, reference_unit):
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(reference_unit)
    hx.reset()
    hx.tare()
    lcd.writeString("Taring done")
    #sleep(1)
    lcd.clear()
    print("Taring done...")

def hx_readvalue(hx):
    val = hx.get_weight()
    print(roundvalue(val))
    #hx.power_down()
    #hx.power_up()
    return roundvalue(val)

def roundvalue(value):
    return round(value)
    
def model_paths_exists(model_path, classnames_path):
    if not os.path.exists(model_path) or not os.path.exists(classnames_path):
        print("Model doesn't exist, take pictures and train it first")
        return False
    else:
        return True

if __name__ == "__main__":
    main()
