import cv2
import uuid
import os
import time
import sys
#import msvcrt
import numpy as np
import select

picture_size = 128
def display_picture():
    # Displays videoimage until enter is pressed on keyboard (command prompt as active window)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('frame', frame)
            if heardEnter():
                break
            cv2.waitKey(25)
        else:
            break

#    cap.release()
    cv2.destroyAllWindows()

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


picture_name = sys.argv[1]
IMAGES_PATH = os.path.join(os.getcwd(),'..', 'images', 'testimages')
#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap = cv2.VideoCapture(0)
if not os.path.exists(IMAGES_PATH):
    os.makedirs(IMAGES_PATH)

display_picture()

for i in range(1,0,-1):
    print("Taking picture of " + picture_name + ' in ' + str(i) + "s")
    time.sleep(1)

ret, frame = cap.read()
IMAGE_PATH = os.path.join(IMAGES_PATH, picture_name + str(uuid.uuid1()) + '.jpg')

#resize image
frame = crop_square(frame)
cv2.imwrite(IMAGE_PATH, frame)
cv2.imshow('frame', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
