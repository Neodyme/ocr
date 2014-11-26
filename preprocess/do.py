#!/usr/bin/env python2.7
#-*- encoding: utf-8 -*-

import cv2
import numpy as np


TARGET_WIDTH = 32
TARGET_HEIGHT = 32

#
# Crop the letter to let a minimum of white on screen
def crop(img):
    height, width = img.shape

    min_height = height
    max_height = 0
    min_width = width
    max_width = 0

    for i in range(0, height):
        for j in range(0, width):
            if img[i, j] == 0:
                if j < min_height:
                    min_height = j
                if j > max_height:
                    max_height = j
                if i < min_width:
                    min_width = i
                if i > max_width:
                    max_width = i
#    print(min_height, max_height, min_width, max_width)
    img_crop = img[min_width:max_width, min_height:max_height]
#    cv2.imshow('preprocess: after crop', img_crop)
#    cv2.waitKey(0)

    return img_crop

#
# Resize the image to a fixed dimension define by TARGET_WIDTH and TARGET_HEIGHT
def resize(img):
    if img.size <= 0:
        return [[-1]]
    img_resize = cv2.resize(img, (TARGET_WIDTH, TARGET_HEIGHT))
    return img_resize

#
# 
def erode(img):
    kernel = np.ones((1, 1), np.uint8)
    erosion = cv2.erode(img, kernel,iterations = 1)

#    cv2.imshow('preprocess: after erode', erosion)
#    cv2.waitKey(0)

    return (erosion)
    
#
# Converti la l'image en n&b
def threshold(img):
#    cv2.imshow('preprocess: before bw', img)
#    cv2.waitKey(0)

    blur = cv2.GaussianBlur(img,(1,1),0)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#    cv2.imshow('preprocess: after bw', th3)
#    cv2.waitKey(0)

    return th3
#
# execute le preprocessing

def process_text(filename):
    img = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    img = threshold(img)
    return img
    
def process_text_graysacale(filename):
    img = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    img = threshold(img)
    return img


def process_char(img):
    img = threshold(img)
    img = erode(img)
    img = threshold(img)
    img = crop(img)
    img = resize(img)
    return img
    
