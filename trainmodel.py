# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 13:18:39 2019

@author: Hemanshu Namdeo
"""

from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
#from keras.optimizers import rmsprop
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from keras.preprocessing.image import img_to_array
from ImageScraper.cannyedge import cannyedge
from keras.utils import to_categorical
from Imgclassify.lenet import mymodel
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import pickle
import random
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset")
ap.add_argument("-m", "--model", required=True,
	help="path to output model")
ap.add_argument("-l", "--labelbin", required=True,
	help="path to output label binarizer")
ap.add_argument("-p", "--plot", type=str, default="plot.png",
	help="path to output accuracy/loss plot")
args = vars(ap.parse_args())

EPOCHS = 200
INIT_LR = 1e-3
BS = 32

print("[INFO] loading images...")
data = []
labels = []

imagePaths = sorted(list(paths.list_images(args["dataset"])))
random.seed(42)
random.shuffle(imagePaths)
for imagePath in imagePaths:
    image = cv2.imread(imagePath)
#    print(imagePath)
    #time.sleep(5)
    try:
        width,height=image.shape[:2]
#        if width<350 or height<350:
#            continue
        #print(width,height,imagePath)
        image = cannyedge.build(image,0,0)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        image = img_to_array(image)
        data.append(image)
        label = imagePath.split(os.path.sep)[-2]
        labels.append(label)
    except:
        print("File Not Readable")
#    label = 1 if label == "brands" else 0
    
data = np.array(data, dtype="float32") / 255.0
labels = np.array(labels)

print("[INFO] data matrix: {} images ({:.2f}MB)".format(
	len(imagePaths), data.nbytes / (1024 * 1000.0)))

print("[INFO] class labels:")
lb = LabelBinarizer()
labels = lb.fit_transform(labels)

for (i, label) in enumerate(lb.classes_):
	print("{}. {}".format(i + 1, label))

(trainX, testX, trainY, testY) = train_test_split(data,
	labels, test_size=0.3, random_state=42)

#trainY = to_categorical(trainY, num_classes=len(lb.classes_))
#testY = to_categorical(testY, num_classes=len(lb.classes_))

aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")

print("[INFO] compiling model...")
model=mymodel.build(height=128,width=128,depth=1,classes=len(lb.classes_))
#opt = rmsprop(lr=INIT_LR, decay=INIT_LR / EPOCHS)
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="categorical_crossentropy", optimizer=opt,
	metrics=["accuracy"])
model.summary()
print("[INFO] training network...")
H = model.fit_generator(aug.flow(trainX,trainY,batch_size=BS,shuffle=True),
	validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
	epochs=EPOCHS, verbose=1)
print("[INFO] serializing network...")
model.save(args["model"])

print("[INFO] serializing label binarizer...")
f = open(args["labelbin"], "wb")
f.write(pickle.dumps(lb))
f.close()

plt.style.use("ggplot")
plt.figure()
N = EPOCHS
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
plt.title("Training Loss and Accuracy on brand/Not brand")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig(args["plot"])