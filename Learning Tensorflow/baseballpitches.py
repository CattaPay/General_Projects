import pandas as pd
import numpy as np
#import tensorflow as tf

from sklearn.model_selection import train_test_split

allpitches = pd.read_csv("Learning Tensorflow\\allpitches.csv")


print(allpitches.columns)

#predict where ball will end up
pitchdat = allpitches[['release_speed', 
'release_pos_x', 'release_pos_z',
'release_spin_rate', 'release_pos_y', 'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az', 'sz_top', 'sz_bot']]

pitchlabels = pd.get_dummies(allpitches.zone, prefix = 'zone')

#situationdat = allpitches[['balls', 'strikes', 'on_3b', 'on_2b', 'on_1b', 'outs_when_up']]
def scale(bois):
    return(bois / bois.abs().max())


networkdat = pd.concat([pitchdat, pitchlabels], axis = 1)
networkdat = networkdat.dropna()

print(networkdat)

X = networkdat.iloc[:,:13]
print(X)

y = networkdat.iloc[:,13:].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state = 21)

from tensorflow.keras.layers import Input, Dense, Activation,Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

input_layer = Input(shape = X.shape[1],)
dense_layer_1 = Dense(100, activation='relu')(input_layer)
dense_layer_2 = Dense(100, activation='relu')(dense_layer_1)
dense_layer_3 = Dense(50, activation='relu')(dense_layer_2)
output = Dense(y.shape[1], activation='softmax')(dense_layer_3)

model = Model(inputs = input_layer, outputs = output)
model.compile(loss='categorical_crossentropy', optimizer=Adam(lr = 0.001), metrics=['acc'])

print(model.summary())

history = model.fit(X_train, y_train, batch_size=50, epochs=100, verbose=1, validation_split=0.2)

score = model.evaluate(X_test, y_test, verbose=1)

print("Test Score:", score[0])
print("Test Accuracy:", score[1])

