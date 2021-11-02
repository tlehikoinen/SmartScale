import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow import keras
import numpy as np
import pickle
import os 

class PicturePredicter:
    # When model is trained, it is saved and classnames are written to txt file
    # Give model_path and class_names path as argument and predict picture against the model...
    # ... By calling predictPicture with image path

    def __init__(self, model_path, classnames_path, testpictures_path, picture_path, picture_size=128):
        self.model_path = model_path 
        self.classnames_path = classnames_path 
        self.testpictures_path = testpictures_path
        self.picture_path = picture_path
        self.picture_size = 128
        if not os.path.exists(self.model_path):
            self.modelNotFound()
        else:
            self.classnames = pickle.loads(open(classnames_path, "rb").read())
            self.model = tf.keras.models.load_model(self.model_path)
            self.probability_model = tf.keras.Sequential([self.model, tf.keras.layers.Softmax()])

    def modelNotFound(self):
        input("Trained model not found, train it to use prediction functions...")
        #exit()
         
    def getClassnames(self):
        return self.classnames

    def returnPrediction(self):
        picture = image.load_img(self.picture_path, (self.picture_size, self.picture_size))
        picture = image.img_to_array(picture)
        picture = np.expand_dims(picture,axis=0)
        results = self.probability_model.predict(picture)
        class_number = np.argmax(results)
        class_probability = str(round((np.amax(results)*100), 2))
        print('GUESSES ' + str(self.classnames[class_number]) + ' PROBABILITY = ' + str(class_probability) + '%')
        return self.classnames[class_number]

    def returnFullPredictions(self):
        picture = image.load_img(self.picture_path, (self.picture_size, self.picture_size))
        picture = image.img_to_array(picture)
        picture = np.expand_dims(picture,axis=0)
        results = self.probability_model.predict(picture)
        class_number = np.argmax(results)
        class_probability = str(round((np.amax(results)*100), 2))
        print('GUESSES ' + str(self.classnames[class_number]) + ' PROBABILITY = ' + str(class_probability) + '%')
        flattened_result = np.array(results)
        flattened_result = flattened_result.flatten()
        for count, result in enumerate(flattened_result):
            print('Object name = ' + self.classnames[count] + ' Probability = ' + str(round((result*100), 2)))
    
    def testModel(self):
        test_image_folders = os.listdir(self.testpictures_path)
        for folder in test_image_folders:
            print("\nTesting folder: " + folder)
            pictures = os.listdir(os.path.join(self.testpictures_path, folder))
            for count, picture in enumerate(pictures):
                test_image_path = os.path.join(self.testpictures_path, folder, picture)
                test_image = image.load_img(test_image_path, (self.picture_size, self.picture_size))
                test_image = image.img_to_array(test_image)
                test_image = np.expand_dims(test_image,axis=0)
                result = self.probability_model.predict(test_image)
                self.classnames[np.argmax(result)]
                print(self.classnames[np.argmax(result)] + " " + str(round((np.amax(result)*100), 2)) + " % ---- " + picture)
 
