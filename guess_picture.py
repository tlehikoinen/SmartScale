import cv2
import uuid
import os
import time
import sys
import msvcrt
import numpy as np
import pickle
import os
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing import image

new_model = tf.keras.models.load_model('save_model/mymodel')
class_names = pickle.loads(open('classnames.txt', "rb").read())

print(class_names)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 280)

print('taking picture in 1s')
time.sleep(1)
ret, frame = cap.read()
h, w = frame.shape[:2]
min_size = np.amin([h,w])
size = 128
# Centralize and crop
crop_img = frame[int(h/2-min_size/2):int(h/2+min_size/2), int(w/2-min_size/2):int(w/2+min_size/2)]
resized = cv2.resize(crop_img, dsize=(size, size), interpolation=cv2.INTER_AREA)
print('RESIZED')
print(resized.shape)

probability_model = tf.keras.Sequential([new_model, tf.keras.layers.Softmax()])
test_image = image.img_to_array(resized)
test_image = np.expand_dims(test_image,axis=0)
result = probability_model.predict(test_image)
class_number = np.argmax(result)
class_probability = str(round((np.amax(result)*100), 2))
print(result)
print(class_names[class_number])
print('probability = ' + class_probability)
#training_set.class_indices





#resize image
#new_model.predict(frame)
