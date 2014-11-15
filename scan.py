#!/usr/bin/env python2.7
#-*- encoding: utf-8 -*-
#
# Started on  Thu Oct 30 14:46:24 2014 Prost P.
## Last update Tue Nov 11 21:45:24 2014 Prost P.
#

import cv
import preprocess
import cv2
import preprocess.do
import numpy as np

#
# cycle de scan de caracteres uniques
def scan(filename):
    img = preprocess.do.do(filename)
    return img.astype(np.float32)


#
# cycle de scan de text complet
def scantext(filename):
#    img = preprocess.bounding_word(preprocess.do2(filename))
    img = preprocess.bounding_letter(preprocess.do2(filename))
    return


def knn_dataset(filename='letter-recognition.data'):
    # Load the data, converters convert the letter to a number
    data = np.loadtxt(filename,
                      dtype='float32', delimiter=',',
                      converters={0: lambda ch: ord(ch) - ord('A')})

    # split the data to two, 10000 each for train and test
    train, test = np.vsplit(data, 2)

    # split trainData and testData to features and responses
    responses, trainData = np.hsplit(train, [1])
    labels, testData = np.hsplit(test, [1])

    # Initiate the kNN, classify, measure accuracy.
    knn = cv2.KNearest()
    knn.train(trainData, responses)
    ret, result, neighbours, dist = knn.find_nearest(testData[:1], k=5)

    correct = np.count_nonzero(result == labels)
    accuracy = correct * 100.0 / 10000
    print "ret {}".format(ret)
    print "result {}".format(result)
    print "neighbours {}".format(neighbours)
    print "dist {}".format(dist)
    print "accuracy {}".format(accuracy)
    return knn


def knn_train(files):
    k = np.arange(len(files) / 10)
    train_labels = np.repeat(k, 10)[:, np.newaxis]
    print len(train_labels)
    test_labels = train_labels.copy()
    knn = cv2.KNearest()
    knn.train(imgs, train_labels)
    ret, result, neighbours, dist = knn.find_nearest(imgs, k=5)

    # Now we check the accuracy of classification
    # For that, compare the result with test_labels and check which are wrong
    matches = result == test_labels
    correct = np.count_nonzero(matches)
    accuracy = correct * 100.0 / result.size
    print accuracy


def knn_find(knn, files):
    f = np.asmatrix(files)
    f = [f]
    ret, result, neighbours, dist = knn.find_nearest(f, k=5)
    # correct = np.count_nonzero(result == labels)
    # accuracy = correct * 100.0 / 10000
    print "ret {}".format(ret)
    print "result {}".format(result)
    print "neighbours {}".format(neighbours)
    print "dist {}".format(dist)
    # print "accuracy {}".format(accuracy)
