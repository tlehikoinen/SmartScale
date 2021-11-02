import os
from modules.smartscale import PictureTaker, PictureTakerWithClass, PriceHandler, Menu
from modules.litepredicter import PicturePredicterLite
import modules.config as cf

def main():
    model_path = cf.lite_model_path
    classnames_path = cf.classnames_path
    testpicture_path = cf.testpicture_path 
    images_folder = cf.images_folder 
    root_image_path = cf.root_image_path
    prices_path = cf.prices_path 

    # If model doesn't exists, user can only access menu from which pictures can be taken with classnames
    modelExists = model_paths_exists(model_path, classnames_path)
    picturetaker = PictureTaker(testpicture_path)

    if modelExists:
        predicter = PicturePredicterLite(model_path, classnames_path, testpicture_path)
        pricehandler = PriceHandler(prices_path, predicter.getClassnames())
        helpmenu = Menu(['How to take pictures', 'How to predict pictures', 'How to change prices'])
    else:
        print("Model was not found")
        exit()

    continueProgram = True

    while(continueProgram):
        selection = input("\nPICTURE MENU\n1. Take picture and print data\n2. Display camera\n3. Go back to main menu")
        if selection == '1':
            picturetaker.takePicture()
            guess = predicter.returnPrediction()
            price = pricehandler.returnPrice(guess)
            print("Product: " + guess + " Price: " + str(price))
        elif selection == '2':
            picturetaker.displayPicture()
        elif selection == '3':
            # Returning so user is not asked to press key to continue
            continueProgram = False
            return
        else:
            print("Wrong input, try again")
        input("\nPress enter key to continue\n")

def model_paths_exists(model_path, classnames_path):
    if not os.path.exists(model_path) or not os.path.exists(classnames_path):
        print("Model doesn't exist, take pictures and train it first")
        return False
    else:
        return True

if __name__ == "__main__":
    main()
