import cv2
import uuid
import os
import time
import sys
import numpy as np
import select 

try:
    if sys.argv[1] == "test":
        IMAGES_PATH = os.path.join(os.getcwd(),'..', 'images', 'testhandsigns')
        print("TAKING PICTURES TO TESTFOLDER")
except:
    IMAGES_PATH = os.path.join(os.getcwd(),'..', 'images', 'handsigns')
    print("TAKING PICTURES TO REGULAR FOLDER")
cap = cv2.VideoCapture(0)
#IMAGES_PATH = os.path.join(os.getcwd(), 'images', 'testhandsigns')
picture_size = 128
picture_delay = 1

def main():

    if not os.path.exists(IMAGES_PATH):
        os.makedirs(IMAGES_PATH)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 280)

    ContinueProgram = True;

    while(ContinueProgram):
        label = input('Take picture by entering label name, or enter q for quit ')
        if(label != 'q'):
            amount = input('How many pictures you want to take(int) ')
            take_picture(label, amount)
        else:
            ContinueProgram = False

def take_picture(label, amount):
    LABELED_PICTURES_PATH = os.path.join(IMAGES_PATH, label)
    if not os.path.exists(LABELED_PICTURES_PATH):
            os.makedirs(LABELED_PICTURES_PATH)
    for i in range(0, int(amount)):
        display_picture()

        for j in range(int(picture_delay),0,-1):
            print("Taking picture of " + str(label) + " in " + str(j) + "s")
            time.sleep(1)

        ret, frame = cap.read()
        IMAGE_PATH = os.path.join(LABELED_PICTURES_PATH, str(uuid.uuid1()) + '.jpg')

        #resize image
        frame = crop_square(frame)
        cv2.imwrite(IMAGE_PATH, frame)
        cv2.imshow('frame', frame)
        
        if i == int(amount) -1:
            #cv2.waitKey(0)
            cv2.destroyAllWindows()

def display_picture():
    # Displays videoimage until ESC is pressed on keyboard (command prompt as active window)
    print("Take picture by pressing enter")
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('frame', frame)
            if heardEnter() == True:
                break
            cv2.waitKey(25)
        else:
            break

#    cap.release()
    #cv2.destroyAllWindows()

def crop_square(img, size=picture_size, interpolation=cv2.INTER_AREA):
    h, w = img.shape[:2]
    min_size = np.amin([h,w])

    # Centralize and crop
    crop_img = img[int(h/2-min_size/2):int(h/2+min_size/2), int(w/2-min_size/2):int(w/2+min_size/2)]
    resized = cv2.resize(crop_img, (size, size), interpolation=interpolation)

    return resized

def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False

if __name__ == "__main__":
    main()
