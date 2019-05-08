# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 16:33:20 2019

@author: Hemanshu Namdeo
"""

import cv2
image=cv2.imread('C:\\Users\\Hemanshu Namdeo\\.spyder-py3\\Images\\ball.jpg')
h,w=image.shape[:2]
print(h,w)
image=cv2.resize(image,(512,512))
nh,nw=image.shape[:2]
center=(int(h*0.5),int(w*0.5))
cv2.imshow('Output',image)
cv2.waitKey(0)

#imag=cv2.resize(image,(w,h))
print(center)
#img=image[(center[0]-int(center[0]/2)):(center[0] + int(center[0]/2)),(center[1]-int(center[1]/2)):(center[1] + int(center[1]/2))]
#img=image[0:center[0],0:center[1]]
img=image[int(center[0]*0.5):int(1.5*center[0]),int(0.5*center[1]):int(1.5*center[1])]
img=cv2.resize(img,(512,512))
cv2.imshow('Output',img)
cv2.waitKey(0)