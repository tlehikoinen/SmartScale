import os
from smartscale import PicturePredicter, PictureTaker, PictureTakerWithClass, PriceHandler, Menu

def main():
    model_path = os.path.join(os.getcwd(),"saved_model","mymodel")
    classnames_path = os.path.join(os.getcwd(),"classnames.txt")
    testpicture_path = os.path.join(os.getcwd(),"images", "testimages", "predictpicture.jpg")
    images_folder = os.path.join(os.getcwd(), "images", "handsigns")
    prices_path = os.path.join(os.getcwd(), "pricelist.csv")

    predicter = PicturePredicter(model_path, classnames_path, testpicture_path)
    picturetaker = PictureTaker(testpicture_path)
    pricehandler = PriceHandler(prices_path, predicter.getClassnames())
    classtaker = PictureTakerWithClass(images_folder)
    helpmenu = Menu(['How to take pictures', 'How to predict pictures', 'How to change prices'])
    continueProgram = True
	
    while(continueProgram):
        print("\nMAIN MENU\nWhat do you want to do")
        selection = input("1. Open picture menu\n2. Open price menu\n3. Open picture with class menu\n4. Help\n5. Quit")
        if selection == '1':
            # Open menu from which you can take, predict or view cameras picture
            pictureMenu(picturetaker, predicter, pricehandler)
        elif selection == '2':
            pricehandler.menu()
        elif selection == '3':
            classtaker.menu()
        elif selection == '4':
            print("Maybe add help (also for submenus)")
            helpmenu.display()
        elif selection == '5':
            continueProgram = False
            exit()
        else:
            print("Wront input, try again")
        #input("\nPress enter to key to continue\n")

def pictureMenu(picturetaker, predicter, pricehandler):
    continueProgram = True

    while(continueProgram):
        selection = input("\nPICTURE MENU\n1. Take picture and print data\n2. Take picture and print weights\n3. Display camera\n4. Go back to main menu")
        if selection == '1':
            picturetaker.takePicture()
            guess = predicter.returnPrediction()
            price = pricehandler.returnPrice(guess)
            print("Product: " + guess + " Price: " + str(price))
        elif selection == '2':
            picturetaker.takePicture()
            predicter.returnFullPredictions()
        elif selection == '3':
            picturetaker.displayPicture()
        elif selection == '4':
            # Returning so user is not asked to press key to continue
            continueProgram = False
            return
        else:
            print("Wrong input, try again")
        input("\nPress enter key to continue\n")
if __name__ == "__main__":
    main()
