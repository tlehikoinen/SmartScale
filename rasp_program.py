import os
from modules.smartscale import PicturePredicter, PictureTaker, PictureTakerWithClass, PriceHandler, Menu
from modules.raspberry import LcdHandler
import modules.cf as cf

def main():
    model_path = cf.model_path
    classnames_path = cf.classnames_path
    testpicture_path = cf.testpicture_path 
    images_folder = cf.images_folder 
    root_image_path = cf.root_image_path
    testimages_folder = cf.testimages_folder
    prices_path = cf.prices_path 

    # If model doesn't exists, user can only access menu from which pictures can be taken with classnames
    modelExists = model_paths_exists(model_path, classnames_path)
    classtaker = PictureTakerWithClass(root_image_path, images_folder, testimages_folder)
    picturetaker = PictureTaker(testpicture_path)

    if modelExists:
        classtaker.no_model = False
        predicter = PicturePredicter(model_path, classnames_path, testimages_folder, testpicture_path)
        pricehandler = PriceHandler(prices_path, predicter.getClassnames())
        helpmenu = Menu(['How to take pictures', 'How to predict pictures', 'How to change prices'])
        lcd = LcdHandler()

    continueProgram = True

    while(continueProgram):
        if modelExists:
            print("\nMAIN MENU\nWhat do you want to do")
            selection = input("1. Open picture menu\n2. Open price menu\n3. Open picture with class menu\n4. Help\n5. Quit")
            if selection == '1':
                # Open menu from which you can take, predict or view cameras picture
                pictureMenu(picturetaker, predicter, pricehandler, lcd)
            elif selection == '2':
                pricehandler.menu()
            elif selection == '3':
                classtaker.menu()
            elif selection == '4':
                print("Maybe add help (also for submenus)")
                helpmenu.display()
            elif selection == '5':
                continueProgram = False
                lcd.stop()
                exit()
            else:
                print("Wront input, try again")
            #input("\nPress enter to key to continue\n")
        else:
            classtaker.menu()

def model_paths_exists(model_path, classnames_path):
    if not os.path.exists(model_path) or not os.path.exists(classnames_path):
        print("not")
        return False
    else:
        print("yes")
        return True

def pictureMenu(picturetaker, predicter, pricehandler, lcd):
    continueProgram = True

    while(continueProgram):
        selection = input("\nPICTURE MENU\n1. Take picture and print data\n2. Take picture and print weights\n3. Display camera\n4. Test model\n5. Go back to main menu")
        if selection == '1':
            picturetaker.takePicture()
            guess = predicter.returnPrediction()
            price = pricehandler.returnPrice(guess)
            lcd.writeString(guess + " " +  str(price) + "e")
            print("Product: " + guess + " Price: " + str(price))
        elif selection == '2':
            picturetaker.takePicture()
            predicter.returnFullPredictions()
        elif selection == '3':
            picturetaker.displayPicture()
        elif selection == '4':
            predicter.testModel()
        elif selection == '5':
            # Returning so user is not asked to press key to continue
            continueProgram = False
            return
        else:
            print("Wrong input, try again")
        input("\nPress enter key to continue\n")

if __name__ == "__main__":
    main()
