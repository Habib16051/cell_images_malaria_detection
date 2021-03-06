# -*- coding: utf-8 -*-
"""Cell images malaria detetction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_JjEIax8vmvacBlmj3m-foC7VuKom7MP
"""

from tensorflow.keras.layers import Input, Lambda,Dense, Flatten, Conv2D
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt

# re-size all the image to this

IMAGE_SIZE = [224,244]

train_path = '/content/drive/MyDrive/Malaria Detection/Dataset/Train'
valid_path = '/content/drive/MyDrive/Malaria Detection/Dataset/Test'

vgg19 = VGG19(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

vgg19.summary()

# don't train existing weights
for layer in vgg19.layers:
  layer.trainable = False

# useful for getting number of output classes
folders = glob('/content/drive/MyDrive/Malaria Detection/Dataset/Train/*')

folders

# Our Layers - You can add more if you want
 x = Flatten()(vgg19.output)

prediction = Dense(len(folders), activation='softmax')(x)

# create a model object
model = Model(inputs=vgg19.input, outputs=prediction)

# view the structure of model
model.summary()

from tensorflow.keras.layers import MaxPooling2D

# Create Model from scratch using CNN
model = Sequential()
model.add(Conv2D(filters=16, kernel_size=2, padding='same',activation='relu', input_shape=(224,224,3)))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=32,kernel_size=2,padding='same',activation='relu'))


model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=64,kernel_size=2,padding='same',activation='relu'))
model.add(MaxPooling2D(pool_size=2))

model.add(Flatten())

model.add(Dense(500,activation='relu'))
model.add(Dense(2,activation='softmax'))
model.summary()

# tell the model what cost and optimization method to use

model.compile(
    loss = 'categorical_crossentropy',
    optimizer = 'adam',
    metrics = ['accuracy']

)

# Use the image Data Generator to import the images from dataset
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)
test_datagen = ImageDataGenerator(rescale = 1./255)

# Make sure you provide the same target size as initialized for the image

training_set = train_datagen.flow_from_directory('/content/drive/MyDrive/Malaria Detection/Dataset/Train',
                                                 target_size=(224,224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical'
                                                 )

training_set

test_set = train_datagen.flow_from_directory('/content/drive/MyDrive/Malaria Detection/Dataset/Test',
                                                 target_size=(224,224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical'
                                                 )

# fit the model

# Run the cell. It will take sometime to execute

r = model.fit(
    training_set,
    validation_data = test_set,
    epochs = 50,
    steps_per_epoch = len(training_set),
    validation_steps = len(test_set)
)

# loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()
plt.savefig('LossVal_loss')

# accuracies
plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()
plt.savefig('AccVal_acc')

import tensorflow as tf

from keras.models import load_model

model.save('model_vgg19.h5')

