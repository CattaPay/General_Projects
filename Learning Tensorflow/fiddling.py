import pandas as pd
import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split

print("hi")

cols = ['price', 'maint', 'doors', 'persons', 'lug_capacity', 'safety','output']

cars = pd.read_csv("Learning Tensorflow\\car_evaluation.csv", header = None, names = cols)

print(cars.head())

price = pd.get_dummies(cars.price, prefix = "price")
maint = pd.get_dummies(cars.maint, prefix = "maint")
doors = pd.get_dummies(cars.doors, prefix = "doors")
persons = pd.get_dummies(cars.persons, prefix = "persons")
lug_capacity = pd.get_dummies(cars.lug_capacity, prefix = "lug_capacity")
safety = pd.get_dummies(cars.safety, prefix = "safety")
labels = pd.get_dummies(cars.output, prefix = "condition")


X = pd.concat([price, maint, doors, persons, lug_capacity, safety], axis = 1)

y = labels.values



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state = 42)

from tensorflow.keras.layers import Input, Dense, Activation,Dropout
from tensorflow.keras.models import Model

input_layer = Input(shape = X.shape[1],)
dense_layer_1 = Dense(100, activation='relu')(input_layer)
dense_layer_2 = Dense(100, activation='relu')(dense_layer_1)
dense_layer_3 = Dense(50, activation='relu')(dense_layer_2)
output = Dense(y.shape[1], activation='softmax')(dense_layer_3)

model = Model(inputs = input_layer, outputs = output)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])

print(model.summary())

history = model.fit(X_train, y_train, batch_size=8, epochs=50, verbose=1, validation_split=0.2)

score = model.evaluate(X_test, y_test, verbose=1)

print("Test Score:", score[0])
print("Test Accuracy:", score[1])

