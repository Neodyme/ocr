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
def scan(knn, filename, p):
    img = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    c = img.copy()
    img = preprocess.process_char(img)
    if img[0][0] == -1:
        return
    img = [img.reshape(-1, 1)]
    ret, result, neighbours, dist = knn.find_nearest(numpy.float32(img), 10)
    if int(dist[0][0]) != 0:
        result2 = p.sift(c)
        result3 = p.surf(c)
        neigh = neighbours.tolist()[0]
        di = dist.tolist()[0]
        neigh = [ord(chr(int(x)).lower()) for x in neigh]
        result2 = [(x[0].lower(), x[1]) for x in result2]
        result3 = [(x[0].lower(), x[1]) for x in result3]
        for r in result2:
            let = ord(r[0])
            if  let in neighbours:
                di[neigh.index(let)] = di[neigh.index(let)] - (di[neigh.index(let)]) * 0.10 * ((r[1] / 100))
        for r in result3:
            let = ord(r[0])
            if  let in neighbours:
                di[neigh.index(let)] = di[neigh.index(let)] - (di[neigh.index(let)]) * 0.10 * ((r[1] / 100))
        mini = di[0]
        index = 0
        n = 0
        for l in range(len(neigh)):
            for l2 in range(len(neigh)):
                if l != l2 and neigh[l] == neigh[l2]:
                    di[l] = di[l] * 0.95
        for i in di:
            if i < mini:
                mini = i
                index = n
            n += 1
        res = neighbours[0][index]
    else:
        res = neighbours[0][0]
    print(chr(int(res)))
    return chr(int(res))

#
# cycle de scan de text complet
def scantext(knn, filename, p):
    lines = preprocess.bounding_word(cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE), filename)
    l = []
    for line in lines:
        words = []
        for word in line:
            chars, _ = preprocess.bounding_letter(word)
            words.append(chars)
        l.append(words)
    return findLetter(knn, l, p)

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
        print("learning {0:.02%} ".format(float(i) / float(len (files))))
        imgList.append(preprocess.process_char(cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)).reshape(-1, 1))
        imgTag.append(ord(path.basename(filename)[0]))
        i += 1
    knn.train(numpy.float32(imgList), numpy.float32(imgTag))
    return knn

def findLetter(knn, lines, p):
    message = ""
    for line in lines:
        for word in line:
            for c in word:
                img = preprocess.process_char(c)
                if img[0][0] == -1:
                    continue
                img = [img.reshape(-1, 1)]
#                cv2.imshow('2end letter bounding detection', c)
#                cv2.waitKey(0)
                ret, result, neighbours, dist = knn.find_nearest(numpy.float32(img), 10)
                if int(dist[0][0]) != 0:
                    result2 = p.sift(c)
                    result3 = p.surf(c)
                    neigh = neighbours.tolist()[0]
                    di = dist.tolist()[0]
                    neigh = [ord(chr(int(x)).lower()) for x in neigh]
                    result2 = [(x[0].lower(), x[1]) for x in result2]
                    result3 = [(x[0].lower(), x[1]) for x in result3]
                    for r in result2:
                        let = ord(r[0])
                        if  let in neighbours:
                            di[neigh.index(let)] = di[neigh.index(let)] - (di[neigh.index(let)]) * 0.10 * ((r[1] / 100))
                    for r in result3:
                        let = ord(r[0])
                        if  let in neighbours:
                            di[neigh.index(let)] = di[neigh.index(let)] - (di[neigh.index(let)]) * 0.10 * ((r[1] / 100))
                    mini = di[0]
                    index = 0
                    n = 0
                    for l in range(len(neigh)):
                        for l2 in range(len(neigh)):
                            if l != l2 and neigh[l] == neigh[l2]:
                                di[l] = di[l] * 0.95
                            
                    for i in di:
                        if i < mini:
                            mini = i
                            index = n
                        n += 1
                    res = neighbours[0][index]
                else:
                    res = neighbours[0][0]
                message += chr(int(res))
                print(message)
            message += " "
        message += "\n"
    print (message)
    return message
