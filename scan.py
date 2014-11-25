#!/usr/bin/env python2.7
#-*- encoding: utf-8 -*-
# 
# Started on  Thu Oct 30 14:46:24 2014 Prost P.
## Last update Tue Nov 25 20:56:08 2014 Prost P.
#

import cv2
import preprocess
import numpy
from os import path
from glob import glob
#
# cycle de scan de caracteres uniques
def scan(filename):
    img = preprocess.process_char(filename)
    return
#
# cycle de scan de text complet
def scantext(filename):
    lines = preprocess.bounding_word(cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE), filename)
    for line in lines:
        for word in line:
            img = preprocess.bounding_letter(word)
    return

#
# cycle d'apprentissage de lettre
def learnLetter(directory = "./dataset/"):
    knn = cv2.KNearest()
    imgList = []
    imgTag = []
    i = 0
    for filename in glob(path.join(directory, '*.bmp')):
#        print(filename)
        imgList.append(preprocess.process_char(filename).reshape(-1, 1))
#        print(path.basename(filename)[0])
        imgTag.append(ord(path.basename(filename)[0]))
        i += 1
#    print(numpy.array(imgList).astype(numpy.float64))
 #   print(numpy.array(imgTag).astype(numpy.float64))
    knn.train(numpy.float32(imgList), numpy.float32(imgTag))
    img = [preprocess.process_char("./dataset/P.bmp").reshape(-1, 1)]
    ret, result, neighbours, dist = knn.find_nearest(numpy.float32(img), 3)
    print(result, neighbours, dist)
    return knn
