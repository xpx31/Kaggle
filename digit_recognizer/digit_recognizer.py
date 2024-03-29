"""

Script Description:
	MNIST ("Modified National Institute of Standards and Technology")
	is the de facto “hello world” dataset of computer vision. Since its
	release in 1999, this classic dataset of handwritten images has served
	as the basis for benchmarking classification algorithms. As new
	machine learning techniques emerge, MNIST remains a reliable resource
	for researchers and learners alike.

	In this competition, your goal is to correctly identify digits from a
	dataset of tens of thousands of handwritten images. We’ve curated a set
	of tutorial-style kernels which cover everything from regression to neural
	networks. We encourage you to experiment with different algorithms to
	learn first-hand what works well and how techniques compare.

	https://www.kaggle.com/c/digit-recognizer/overview/description

	Save data file under the same directory and in folder named "Data"

	Sequential neural network portion tutorial followed:
	https://www.tensorflow.org/tutorials/quickstart/beginner


Created by Pengxiang Xu
Date: Oct/05/2019
Time: 20:30
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical

# ML algorithm selection
#   0 - Sequential Neural Network
#   1 - CNN
ml_selection = 1


def nomarlization(X):
	# Normalization
	X /= np.max(X)
	X -= np.std(X)

	return X


def linear_model(Xtrain, ytrain):
	# Normalization
	Xtrain = nomarlization(Xtrain)

	# Construct sequential neural network
	model = tf.keras.models.Sequential([
		tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
		tf.keras.layers.Dense(128, activation='relu'),
		tf.keras.layers.Dropout(0.2),
		tf.keras.layers.Dense(10, activation='softmax')
	])

	# Define optimizer, loss function, and metrics
	model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

	# Cross Validation
	X_train, X_val, y_train, y_val = train_test_split(Xtrain, ytrain, test_size=0.10)

	# Training and evaluation
	model.fit(X_train, y_train, epochs=5)
	model.evaluate(X_val, y_val, verbose=2)

	return model


def cnn(Xtrain, ytrain):
	# Construct CNN model
	model = tf.keras.models.Sequential([
		tf.keras.layers.Convolution2D(32, (3, 3), activation='relu'),
		tf.keras.layers.Convolution2D(32, (3, 3), activation='relu'),
		tf.keras.layers.MaxPooling2D(),
		tf.keras.layers.Convolution2D(64, (3, 3), activation='relu'),
		tf.keras.layers.Convolution2D(64, (3, 3), activation='relu'),
		tf.keras.layers.MaxPooling2D(),
		tf.keras.layers.Flatten(),
		tf.keras.layers.Dense(512, activation='relu'),
		tf.keras.layers.Dense(10, activation='softmax')
	])

	model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

	# Cross Validation
	X_train, X_val, y_train, y_val = train_test_split(Xtrain, ytrain, test_size=0.10, random_state=42)

	# Training and evaluation
	model.fit(X_train, y_train, epochs=5)
	model.evaluate(X_val, y_val, verbose=1)

	return model


# Load Data
input_path = "./Data/"
data_train = pd.read_csv(input_path + "train.csv")
data_test = pd.read_csv(input_path + "test.csv")

# Get features and labels
X_train = data_train.iloc[:, 1:].values.astype('float32')
y_train = data_train.iloc[:, 0].values.astype('float32')
X_test = data_test.values.astype('float32')

# Each image contains 28 x 28 pixels, add 1 dimension for color channel gray
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)

# Get categories from labels
y_train = to_categorical(y_train)

# Run model
model = tf.keras.models.Sequential()
if ml_selection is 0:
	model = linear_model(X_train, y_train)
elif ml_selection is 1:
	model = cnn(X_train, y_train)
else:
	print("Select a model to run")
	exit(1)

# Prediction
print("Prediction")
predction = model.predict_classes(X_test, verbose=1)

submissions=pd.DataFrame({"ImageId": list(range(1,len(predction)+1)),
                         "Label": predction})
submissions.to_csv("prediction.csv", index=False, header=True)