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
import numpy as np
import argparse
import imutils
import cv2

#cgitb.enable()
#form = cgi.FieldStorage()
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to trained model model")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())
#fileitem = form['filename']

image = cv2.imread(args["image"])
#image=cv2.imread(fileitem)
width,height=image.shape[:2]
orig = image.copy()

image = cv2.resize(image, (96, 96))
image = image.astype("float") / 255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

print("[INFO] loading network...")
model = load_model(args["model"])
#model = load_model("brands.model")
(notbrand, brand) = model.predict(image)[0]
print(brand)
print(notbrand)
label = "Brand" if brand > notbrand else "Not Brand"
proba = brand if brand > notbrand else notbrand
label = "{}: {:.2f}%".format(label, proba * 100)
output = imutils.resize(orig, width=400)
cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
	0.7, (0, 0, 255), 2)
cv2.imshow("Output", output)
cv2.waitKey(0)
cv2.destroyWindow()
