import cv2
import uuid
import os
import time
import sys
import msvcrt
import numpy as np
import pickle
import tensorflow as tf
from keras.preprocessing import image
from tensorflow import keras


new_model = tf.keras.models.load_model('../saved_model/mymodel')
probability_model = tf.keras.Sequential([new_model, tf.keras.layers.Softmax()])
class_names = pickle.loads(open('../classnames.txt', "rb").read())

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
test_image_path = os.path.join(os.getcwd(), '..', 'images', 'testimages', 'test.jpg')
picture_size = 128
picture_delay = 1
def main():

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 280)

    ContinueProgram = True;

    while(ContinueProgram):
        predict_picture()

def predict_picture():
    display_picture()

    ret, frame = cap.read()
    cv2.imshow('frame', frame)

    #resize image
    frame = crop_square(frame)
    cv2.imwrite(test_image_path, frame)
    #cv2.waitKey(0)    
    test_image = image.load_img(test_image_path, (128, 128))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image,axis=0)
    result = probability_model.predict(test_image)
    class_number = np.argmax(result)
    class_probability = str(round((np.amax(result)*100), 2))
    print('ORIGINAL RESULT ' + str(result))
    print('CLASS NUMBER ' + str(class_names[class_number]))
    print('PROBABILITY = ' + str(class_probability))
    time.sleep(1)

def display_picture():
    # Displays videoimage until ESC is pressed on keyboard (command prompt as active window)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('frame', frame)
            if msvcrt.kbhit():
                if ord(msvcrt.getch()) == 27:
                    break;
            cv2.waitKey(25)
        else:
            break

#    cap.release()
#    cv2.destroyAllWindows()

def crop_square(img, size=picture_size, interpolation=cv2.INTER_AREA):
    h, w = img.shape[:2]
    min_size = np.amin([h,w])

    # Centralize and crop
    crop_img = img[int(h/2-min_size/2):int(h/2+min_size/2), int(w/2-min_size/2):int(w/2+min_size/2)]
    resized = cv2.resize(crop_img, (size, size), interpolation=interpolation)

    return resized

if __name__ == "__main__":
    main()
