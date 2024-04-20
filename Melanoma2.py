
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelBinarizer
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from sklearn.metrics import accuracy_score

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
#from sklearn.utils.multiclass import unique_labels
from keras.models import load_model
import tensorflow as tf 
from keras.utils import to_categorical
veri=pd.read_csv("hmnist_28_28_L.CSV")



#y=ax+b

y=veri["label"].values

x=veri.drop("label",axis=1).values


x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=100)
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
x_train=x_train/255
x_test=x_test/255
                                           
num_classes = 7
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

    
model = Sequential()
model.add(Conv2D(64, kernel_size=(3,3), activation = 'relu', input_shape=(28, 28 ,1) )) 
model.add(MaxPooling2D(pool_size = (2, 2)))

model.add(Conv2D(64, kernel_size = (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))

model.add(Conv2D(64, kernel_size = (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))

model.add(Flatten())
model.add(Dense(128, activation = 'relu'))


model.add(Dropout(0.20))
model.add(Dense(num_classes, activation = 'softmax'))
model.compile(loss = keras.losses.categorical_crossentropy, optimizer=tf.optimizers.Adam(),metrics=['accuracy'])

    
#history = model.fit(x_train, y_train, validation_data = (x_train, y_train), epochs=200, batch_size=32)

#model.save_weights("my_modelweightss")



