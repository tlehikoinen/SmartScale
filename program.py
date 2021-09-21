import os
from Price import PicturePredicter, PictureTaker, PriceHandler

def main():
    model_path = os.path.join(os.getcwd(),"saved_model","mymodel")
    classnames_path = os.path.join(os.getcwd(),"classnames.txt")
    testpicture_path = os.path.join(os.getcwd(),"images", "testimages", "coffeecup1c9a13b4-10ae-11ec-8ce8-2c4d544e1729.jpg")
    prices_path = os.path.join(os.getcwd(), "pricelist.csv")

    predicter = PicturePredicter(model_path, classnames_path, testpicture_path)
    picturetaker = PictureTaker(testpicture_path)
    pricehandler = PriceHandler(prices_path, predicter.getClassnames())

    continueProgram = True

    while(continueProgram):
        print("What do you want to do")
        selection = input("1. Take picture and print data\n2. Take picture and print weights\n3. Open price menu\n4. Quit\n")
        if selection == '1':
            picturetaker.takePicture()
            guess = predicter.returnPrediction()
            price = pricehandler.returnPrice(guess)
            print("Product: " + guess + " Price: " + str(price))
        elif selection == '2':
            picturetaker.takePicture()
            predicter.returnFullPredictions()
        elif selection == '3':
            pricehandler.menu()
        elif selection == '4':
            continueProgram = False
        else:
            print("Wront input, try again")
        input("\nPress any key to continue\n")

if __name__ == "__main__":
    main()

