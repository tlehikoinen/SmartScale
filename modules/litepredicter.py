import os
import numpy as np
import tflite_runtime.interpreter as tflite
import pickle
from numpy import asarray
from PIL import Image

class PicturePredicterLite:
    def __init__(self, model_path, classnames_path, picture_path):
        #self.model_path = model_path
        #self.classnames_path = classnames_path
        self.picture_path = picture_path
        self.interpreter = tflite.Interpreter(model_path)
        self.interpreter.allocate_tensors()
        self.picture_size = 128
        self.classnames = pickle.loads(open(classnames_path, "rb").read())
    
    def getClassnames(self):
        return self.classnames

    def returnPrediction(self):
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        image = Image.open(self.picture_path)
        image = asarray(image)

        image = image.astype(np.float32)
        image = np.expand_dims(image, axis=0)
    
        self.interpreter.set_tensor(input_details[0]['index'], image)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(output_details[0]['index'])
        
        print("______________")
        class_number = np.argmax(output_data)
        #class_probability = str(round((np.amax(output_data)*100), 2))
        #print('GUESSES ' + str(self.classnames[class_number]) + ' PROBABILITY = ' + str(class_probability) + '%')
        print('GUESSES ' + str(self.classnames[class_number]))
        return self.classnames[class_number]

    def returnFullPredictions(self):
        pass
 
    def testModel(self):
        pass

    def printInterpreterInfo(self):
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        print("Input Shape:", input_details[0]['shape'])
        print("Input Type:", input_details[0]['dtype'])
        print("Output Shape:", output_details[0]['shape'])
        print("Output Type:", output_details[0]['dtype'])


    def printPictureInfo(self):
        image = Image.open(self.picture_path)
        # summarize some details about the image
        print(image.format)
        print(image.size)
        print(image.mode)

        data = asarray(image)
        print(type(data))
        print(data.shape)
