import cv2
import uuid
import os
import time
import sys
#import msvcrt
import numpy as np
import select


picture_name = sys.argv[1]
IMAGES_PATH = os.path.join(os.getcwd(),'..', 'images', 'testimages')
cap = cv2.VideoCapture(0)
if not os.path.exists(IMAGES_PATH):
    os.makedirs(IMAGES_PATH)

for i in range(3,0,-1):
    print("Taking picture of " + picture_name + ' in ' + str(i) + "s")
    time.sleep(1)

ret, frame = cap.read()
IMAGE_PATH = os.path.join(IMAGES_PATH, picture_name + str(uuid.uuid1()) + '.jpg')

#resize image
cv2.imwrite(IMAGE_PATH, frame)
cv2.waitKey(0)
