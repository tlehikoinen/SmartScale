import os
# os.getcwd points to current directory from which the program is run

# Multiple models can be saved
model_name = "boxes"
litemodel_name = model_name + "_lite"

model_path = os.path.join(os.getcwd(), "saved_model", model_name)
lite_model_path = os.path.join(os.getcwd(), "saved_model", model_name, litemodel_name)
classnames_path = os.path.join(os.getcwd(), "saved_model", model_name, "classnames.txt")
testpicture_path = os.path.join(os.getcwd(), "images", "predictpicture.jpg")
images_folder = os.path.join(os.getcwd(), "images", "classpictures", model_name)
root_image_path = os.path.join(os.getcwd(), "images")
testimages_folder = os.path.join(os.getcwd(), "images", "testimages", model_name)
prices_path = os.path.join(os.getcwd(), "saved_model", model_name, "pricelist.csv")
saved_data_path = os.path.join(os.getcwd(), "saved_model", model_name, "saved_data.csv")

picture_size = 128
cv2_cam = 0





