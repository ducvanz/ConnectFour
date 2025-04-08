from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten
import pickle

model = Sequential()

model.add(Conv2D(filter = 128, kernel_size = (3, 3), padding = "same", activation = "relu", input_shape = (7, 6, 1)))
model.add(Flatten())
model.add(Dense(units = 64, activation = "relu"))
model.add(Dense(units = 64, activation = "relu"))

model.add(Dense(unit = 7, activation = "softmax"))
model.compile(loss='categorical_crossentropy',
                   optimizer='adam', 
                   metrics=['accuracy'])

with open("DL/Files/data.pkl", "rb") as f:
    train, label = pickle.load(f)

model.fit(train, label, epochs = 100, verbose = 1)

model.save("DL/Files/evaluate.h5")

