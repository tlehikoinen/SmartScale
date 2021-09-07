import cv2
import uuid
import os
import time


IMAGES_PATH = os.path.join(os.getcwd(), 'images', 'webcamimages')

if not os.path.exists(IMAGES_PATH):
    os.makedirs(IMAGES_PATH)

cap = cv2.VideoCapture(0)

for i in range(3,0,-1):
    print("Taking picture " + str(i) + "s")
    time.sleep(1)

ret, frame = cap.read()
imgname = os.path.join(IMAGES_PATH, str(uuid.uuid1()) + '.jpg')
print(imgname)
cv2.imwrite(imgname, frame)
cv2.imshow('frame', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
