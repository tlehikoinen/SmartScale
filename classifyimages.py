import os
import csv
import numpy as np

IMAGES_PATH = os.path.join(os.getcwd(), 'images', 'handsigns')
CSV_FILE_PATH = os.path.join(os.getcwd(), 'pictureaddresses.csv')

csvfile =open(CSV_FILE_PATH, 'w', newline='')
writer = csv.writer(csvfile, delimiter=';')
header = ['address', 'class']
writer.writerow(header)
directories = os.listdir(IMAGES_PATH)

for directory in directories:
    HANDSIGN_PATH = os.path.join(IMAGES_PATH, directory)
    print(directory)
    files = os.listdir(HANDSIGN_PATH)
    for file in files:
        SINGLEPICTURE_PATH = os.path.join(HANDSIGN_PATH, file)
        print(file + ' in ' + SINGLEPICTURE_PATH)
        writer.writerow(np.array([SINGLEPICTURE_PATH, directory]))


csvfile.close()
