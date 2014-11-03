#!/usr/bin/env python2.7
#-*- encoding: utf-8 -*-

import cv2

def threshold(img):

    cv2.imshow('preprocess: before bw', img)
    cv2.waitKey(0)
    blur = cv2.GaussianBlur(img,(1,1),0)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    cv2.imshow('preprocess: after bw', th3)
    cv2.waitKey(0)
    return th3

def do(filename):
    img = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    threshold(img)
    return
    
