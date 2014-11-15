#!/usr/bin/env python2.7
#-*- encoding: utf-8 -*-
# 
# Started on  Thu Oct 30 14:46:24 2014 Prost P.
## Last update Tue Nov 11 21:45:24 2014 Prost P.
#

import cv
import preprocess

#
# cycle de scan de caracteres uniques
def scan(filename):
    img = preprocess.do.do(filename)
    return
#
# cycle de scan de text complet
def scantext(filename):
#    img = preprocess.bounding_word(preprocess.do2(filename))
    img = preprocess.bounding_letter(preprocess.do2(filename))
    return
