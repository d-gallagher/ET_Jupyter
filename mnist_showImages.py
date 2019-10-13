import tensorflow as tf
import matplotlib.pyplot as plt

# Simple Program to view training data and test code
# Get the mnist dataset
mnist = tf.keras.datasets.mnist

# Unpack the dataset 
(x_train, y_train), (x_test, y_test) = mnist.load_data()


# Using pyplot to view data as images
# https://stackoverflow.com/questions/2659312/how-do-i-convert-a-numpy-array-to-and-display-an-image
print("Enter which index you want to view. ")
item = input()
plt.imshow(x_train[int(item)], interpolation='nearest')
plt.show()


# Normalize the data to between 0-1
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_train, axis=1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
model.add(tf.keras.layers.Dense(10, activation = tf.nn.relu))
model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=3)
model.save('sgd_TestModel')