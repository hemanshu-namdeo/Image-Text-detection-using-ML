# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 04:21:48 2019

@author: Hemanshu Namdeo
"""
#!"C:\anaconda\Anconda\python.exe"
#import cgi
#import cgitb
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from ImageScraper.cannyedge import cannyedge
import numpy as np
import argparse
import imutils
import pickle
import cv2

#cgitb.enable()
#form = cgi.FieldStorage()
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to trained model model")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-l", "--labelbin", required=True,
	help="path to label binarizer")
args = vars(ap.parse_args())
#fileitem = form['filename']

image = cv2.imread(args["image"])
m=0
pos=0
#image=cv2.imread(fileitem)
width,height=image.shape[:2]
orig = image.copy()

image = cannyedge.build(image,100,200)
#image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow("Intermediate",image)
cv2.waitKey(0)
image = image.astype("float") / 255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

print("[INFO] loading network...")
model = load_model(args["model"])
lb = pickle.loads(open(args["labelbin"], "rb").read())
#model = load_model("brands.model")
print("[INFO] classifying image...")
proba = model.predict(image)[0]
idxs = np.argsort(proba)[::-1][:2]
#(notbrand, brand) = model.predict(image)[0]
#print(brand)
#print(notbrand)
#label = "Brand" if brand > notbrand else "Not Brand"
#proba = brand if brand > notbrand else notbrand
output = imutils.resize(orig, width=400)
for (i, j) in enumerate(idxs):
    if m<proba[j]:
        m=proba[j]
        pos=j
label = "{}: {:.2f}%".format(lb.classes_[pos], proba[pos] * 100)
cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
	0.7, (0, 0, 255), 2)
for (label, p) in zip(lb.classes_, proba):
	print("{}: {:.2f}%".format(label, p * 100))
cv2.imshow("Output", output)
cv2.waitKey(0)
cv2.destroyWindow()
