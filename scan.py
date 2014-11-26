#!/usr/bin/env python2.7
#-*- encoding: utf-8 -*-

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
    l = []
    for line in lines:
        words = []
        for word in line:
            chars = preprocess.bounding_letter(word)
            words.append(chars)
        l.append(words)
    return l

def splitDataset(filename):
    img, _ = preprocess.bounding_letter(preprocess.threshold(cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)))
    let = (path.basename(filename)).split(".")[0]
    i = 0
    print("Filing dataset with letter '{}'".format(let))
    for letter in img:
        if letter.shape[0] > 5 and letter.shape[1] > 5:
            cv2.imwrite("./dataset/" + let + str(i) + ".bmp",  letter)
            i += 1
#
# cycle d'apprentissage de lettre
def learnLetter(directory = "./dataset/"):
    knn = cv2.KNearest()
    imgList = []
    imgTag = []
    i = 0
    for filename in glob(path.join(directory, '*.bmp')):
        # print(filename)
        imgList.append(preprocess.process_char(filename).reshape(-1, 1))
        # print(path.basename(filename)[0])
        imgTag.append(ord(path.basename(filename)[0]))
        i += 1
    # print(numpy.array(imgList).astype(numpy.float64))
    # print(numpy.array(imgTag).astype(numpy.float64))
    knn.train(numpy.float32(imgList), numpy.float32(imgTag))
    return knn

def findLetter(knn, lines):
    for line in lines:
        for words in line:
            for word in words:
                for c in word:
                    img = c.reshape(-1, 1)
                    ret, result, neighbours, dist = knn.find_nearest(numpy.float32(img), 5)
                    print "Expected char: {}".format(test_char)
                    print "Result: {}".format(chr(int(ret)))
                    print "(result: {})".format([chr(int(r)) for r in result])
                    print "Neighbours: {}".format([chr(int(n)) for n in neighbours.reshape(-1, 1)])
                    print "Distances: {}".format(dist)
