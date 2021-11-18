# Smart Scale
On going project about Smart Scale that automatically predicts the item being weighed.  
Python version 3.7.3  

## Setup Instructions
 
Following items are needed:  

-	Raspberry Pi 4+ Model B
-	Load Cell & HX711 
-	16x2 LCD Screen
-	USB Web Camera
-	Metal body

Raspberry Pi (RPi) is the main unit, all the other devices are required to be connected to it. RPi has the following pinout:

<img src="https://user-images.githubusercontent.com/78909617/142463931-7da5324d-1509-49ff-ab0f-de7901c0a7aa.JPG" width="650">


### Raspberry Pi – USB Web Camera
Connect USB Camera to RPi’s USB port.

### Raspberry Pi – LCD Screen
Connect LCD to RPi by following connections:  

<img src="https://user-images.githubusercontent.com/78909617/142464693-431ef1bf-8512-45d6-ad61-9a0ad13a567b.JPG" width="300"> <img src="https://user-images.githubusercontent.com/78909617/142464709-9c78b730-0905-4937-b99a-237d34f5fcf1.JPG" width="350">

**Raspberry Pi** &emsp; **LCD**  
Ground   &emsp;&emsp;  &emsp;&nbsp;GND  
5V power &emsp;&emsp; &ensp;VCC  
Ground	 &emsp; &emsp;&emsp; Vo 	(Contrast adjust, can also be connected to potentiometer)  
GPIO22   &emsp; &emsp;&emsp; RS  
GPIO24	 &emsp; &emsp;&emsp;&nbsp;R/W  
GPIO23	 &emsp; &emsp; &ensp;&nbsp; En  
GPIO9    &emsp; &emsp; &emsp; &nbsp;Data Pin 11  
GPIO25	 &emsp; &emsp; &emsp;Data Pin 12  
GPIO11	 &emsp; &emsp;&emsp; Data Pin 13  
GPIO8	 &emsp; &emsp; &emsp; &nbsp;Data Pin 24  
5V power &emsp; &emsp;&nbsp; Led+  
Ground &emsp; &emsp;&emsp; Led-  

### Raspberry Pi - Load Cell – HX711  
HX711 is a load cell amplifier and connects to both RPi and load cell  

<img src="https://user-images.githubusercontent.com/78909617/142465585-d0c46b32-4a9c-4001-8af0-7453c3a1a2c5.JPG" width="300">

Load cell has four wires with colouring: Red, black, white, green. Connect it to HX711 by following connections:  

**Load Cell** &emsp; &emsp; &ensp; **HX711**  
Red wire &emsp; &emsp; &emsp;RED  
Black wire &emsp; &emsp;  &nbsp; BLK  
White wire &emsp; &emsp; WHT  
Green wire &emsp; &emsp; GRN  

### Metal body
Load cell and camera are connected to metal body.  

## Software Setup

With Git installed clone the software from GitHub with following command:  
*git clone git@github.com:/yellowpasta/infoproject*  
New directory "infoproject" is made with contents of this repository.  

### Installing requirements:
**Windows**  
Follow instructions from the file called “readme.md” in the folder called “windows”.  

**Raspberry Pi**  
Follow instructions from the file called “readme.md” in the folder called “rasp”.  


## Config File  
In “modules” folder, a file called “config.py” (config file) holds the global variables. Before running a program, modify the “model_name” variable. Name of this variable will define the name for folders of pictures and saved classification models. Changing this variable can be used to have multiple models, E.g., one for fruits and the other for candies. Changing this variable name will automatically change all the necessary paths for the program to work.
Variable “cv2_cam” needs to be changed. This will most likely be 1 or 0. Built-in camera in laptops is usually accessed by value 0 and external camera with 1.  


## Running the Program For the First Time
After starting “program.py” or “rasp_program.py” program checks for existing classification model. If it does not exist program continues to “Training menu” from which pictures can be taken and a classification model can be trained. If the model is found, “Main menu” opens from which user has access to all built in features:
-	Take pictures for new and existing items
-	Take a picture and get prediction for it
-	Train a classification model
-	Change prices of items
-	View graphs for data analysis

## Different Programs

After successful installation, depending on the operating system, either “program.py” or “lite_program.py” for Windows, or “rasp_program.py” or “rasp_lite_program.py” for Raspberry Pi can be run.
Programs without “lite_” use full installation of TensorFlow module and can be used to access all the build in features Smart Scale has. Lighter versions (“lite_”) use TensorFlow Lite Runtime module, which is loaded more quickly into the computer’s RAM and predicts items faster.
“trainmodel.py” is a script for training the image classification model and can only be run when a virtual environment with full installation of TensorFlow is activated.
Programs for Windows do not utilize either the LCD or the scale but can be used for taking item pictures or to train the model. The trained model can be then transferred to Raspberry Pi. The idea behind this is that by installing appropriate versions of CUDA and cuDNN and having a suitable Nvidia GPU, the GPU's computational power can be utilized for training the classification model to reduce the time it takes for the script to complete.

## Scale Program
“raspberry_lite_program.py” (Scale program) is the only program from which the main program for running Smart Scale with predictions can be accessed. Other programs are built more into testing and developing the classification model and to access other features such as changing prices or viewing data of sold items. Once Scale program is run, it waits for an item to be placed on the scale and after the item is placed and weight has settled, following events take place:
1.	Program takes a picture and returns a prediction (item name) for it. 
2.	Item name, price and weight are printed to the LCD screen for 1 second, after which product name and total price are displayed.
3.	Data is saved to a file that includes product name, price, weight, and date.
4.	Scale waits until item is removed before changing LCD text to “Place an item”
5.	Scale waits for new item.  

## Frequently Asked Questions:
In this chapter the most common questions and error situations are covered. In case the program does not work as requested, always install requirements following instructions in above chapter called “Software” before further investigation.  

1. Taking a picture result in error code: “Image doesn’t have shape”:
    -	Program does not detect the camera. Change cv2_cam variable in config file from 1 to 0 or vice versa
2.	Pricelist does not have all the products: “Item doesn’t exist”:
    -	Pricelist is only initialised if it does not exist. Retraining the model doesn’t therefore initialise it and user must manually initialise the price list from the menu
3.	Program does not start:
    -	Install all requirements following instructions in above chapter called “Software”
    -	Make sure virtual environment is activated
4.	Training the model using trainmodel.py script result in error:
    -	Errors are usually related to missing pictures and/or folders; Make sure you have at least ten (10) training images and one (1) testing image for each individual image class before running the script.
5.	Smart Scale predicts wrong items:
    -	Accuracy of the model is based on pictures those are taken before training the model, difference of lighting condition in training images vs. predicted image might result in unwanted outcome. It is recommended to have lots of pictures with different positions and lightning conditions to allow for best possible results in predictions
6.	How to calibrate the scale?
    -	Set variable “scale_ref_unit” to 1 in config file
    -	Select “Display scale readings” from Scale Programs menu and place an object with known weight (E.g., 500 g) to scale
    -	Divide the reading of the scale by the objects weight and change “scale_ref_unit” to it (E.g., 220000 / 220 = 1000)
    -	Rerun the Scale program (with empty top) and see if readings are correct
7.	Who made this?
    -	Scale was built by a group of Savonia’s IoT students as a combined project for two courses: Information Technology Project and R&D Development  

### Team members
Tommi Lehikoinen - Project Leader, Software Developer  
Robert Hidri - Hardware Engineer  
Guyangyang Yao - Data Analyst  








