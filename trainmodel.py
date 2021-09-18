#!/usr/bin/env python
# coding: utf-8

# In[1]:

import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import tensorflow_datasets as tfds
from keras.preprocessing import image
from keras.models import save_model
import pickle

if os.path.exists("classnames.txt"):
    os.remove("classnames.txt")

batch_size = 10
img_height = 128
img_width = 128
data_dir = os.path.join(os.getcwd(), 'images', 'handsigns')
testdata_dir = os.path.join(os.getcwd(), 'images', 'testimages')
class_names = None


# In[2]:


train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)


# In[3]:


val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)


# In[4]:


#test_ds = tf.keras.preprocessing.image_dataset_from_directory(
  #testdata_dir,
  #image_size=(img_height, img_width),
  #batch_size=batch_size)


# In[5]:


class_names = train_ds.class_names
print(class_names)
print(len(class_names))
f = open("classnames.txt", "wb")
f.write(pickle.dumps(class_names))
f.close()

# In[6]:


import matplotlib.pyplot as plt

plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
  for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.axis("off")


# In[7]:


for image_batch, labels_batch in train_ds:
  print(image_batch.shape)
  print(labels_batch.shape)
  break


# In[8]:


normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)


# In[9]:


normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixels values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))


# In[10]:


AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)


# In[11]:


num_classes = len(class_names)

model = tf.keras.Sequential([
  tf.keras.layers.experimental.preprocessing.Rescaling(1./255),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(num_classes)
])

model.compile(
  optimizer='adam',
  loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
  metrics=['accuracy'])

model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=5
)


# In[12]:


model.evaluate(val_ds)


# In[13]:

tf.keras.models.save_model(
  model, 'saved_model/mymodel')

probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
individual_pics_test_path = os.path.join(os.getcwd(), 'images', 'testimages')
pic_list = os.listdir(individual_pics_test_path)
for picture in pic_list:
    test_image_path = os.path.join(individual_pics_test_path, picture)
    test_image = image.load_img(test_image_path, (img_height,img_width))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image,axis=0)
    result = probability_model.predict(test_image)
    class_names[np.argmax(result)]
    print(class_names[np.argmax(result)] + " " + str(round((np.amax(result)*100), 2)) + " % ---- " + picture)
    #training_set.class_indices



# ### 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




