#!/usr/bin/env python2.7
#-*- encoding: utf-8 -*-

import cv2
import preprocess
import postprocess
import numpy
from os import path
from glob import glob
#
# cycle de scan de caracteres uniques
def scan(knn, filename):
    img = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    img = preprocess.process_char(img)
    img = [img.reshape(-1, 1)]
#    print img
    ret, result, neighbours, dist = knn.find_nearest(numpy.float32(img), 5)
    print "Result: {}".format(chr(int(ret)))
    print "(result: {})".format([chr(int(r)) for r in result])
    print "Neighbours: {}".format([chr(int(n)) for n in neighbours.reshape(-1, 1)])
    print "Distances: {}".format(dist)
#    cv2.waitKey(0)
    return chr(int(ret))
#
# cycle de scan de text complet
def scantext(knn, filename):
    lines = preprocess.bounding_word(cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE), filename)
    l = []
    for line in lines:
        words = []
        for word in line:
            chars, _ = preprocess.bounding_letter(word)
            words.append(chars)
        l.append(words)
    return findLetter(knn, l)
    

def splitDataset(filename):
    img, _ = preprocess.bounding_letter(preprocess.threshold(cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)))
    let = (path.basename(filename)).split(".")[0]
    i = 0
    print("Filing dataset with letter '{}'".format(let))
    for letter in img:
        if letter.shape[0] > 5 and letter.shape[1] > 5:
            cv2.imwrite("./dataset/" + let + str(i) + ".bmp",  preprocess.erode(preprocess.erode(letter)))
            i += 1
#
# cycle d'apprentissage de lettre
def learnLetter(directory = "./dataset/"):
    knn = cv2.KNearest()
    imgList = []
    imgTag = []
    i = 0
    files = glob(path.join(directory, '*.bmp'))
    for filename in files:
        # print(filename)
        print("learning {0:.02%} ".format(float(i) / float(len (files))))
#        print(cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE).reshape(-1, 1))
#        cv2.imshow('2end letter bounding detection', cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE))
 #       cv2.waitKey(0)
        imgList.append(preprocess.process_char(cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)).reshape(-1, 1))
        # print(path.basename(filename)[0])
        imgTag.append(ord(path.basename(filename)[0]))
        i += 1
    # print(numpy.array(imgList).astype(numpy.float64))
    # print(numpy.array(imgTag).astype(numpy.float64))
    knn.train(numpy.float32(imgList), numpy.float32(imgTag))
    return knn

def findLetter(knn, lines):

    message = ""
    for line in lines:
        for word in line:
            for c in word:
#                print c
                img = preprocess.process_char(c)
                if img[0][0] == -1:
                    continue
                img = [img.reshape(-1, 1)]
#                cv2.imshow('2end letter bounding detection', c)
#                cv2.waitKey(0)

                ret, result, neighbours, dist = knn.find_nearest(numpy.float32(img), 5)
                #                    print "Expected char: {}".format(test_char)

#                message += chr(int(neighbours.reshape(-1, 1)[0]))
                result2 = postprocess.sift.getCharacter(c)
#                for r in result:
#                   if r[0] in 
                print "Result: {}".format(chr(int(ret)))
                print "(result: {})".format([chr(int(r)) for r in result])
                print "Neighbours: {}".format([chr(int(n)) for n in neighbours.reshape(-1, 1)])
                print "Distances: {}".format(dist)
            message += " "
        message += "\n"


    print (message)
    return message
    #                cv2.imshow('3end letter bounding detection', c)
#                cv2.waitKey(0)
#                cv2.imshow('2end letter bounding detection', preprocess.process_char(c))
#                cv2.waitKey(0)
