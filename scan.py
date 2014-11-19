#!/usr/bin/env python2.7
#-*- encoding: utf-8 -*-
# 
# Started on  Thu Oct 30 14:46:24 2014 Prost P.
## Last update Wed Nov 19 14:01:55 2014 Prost P.
#

import cv
import preprocess

#
# cycle de scan de caracteres uniques
def scan(filename):
    img = preprocess.process_char(filename)
    return
#
# cycle de scan de text complet
def scantext(filename):
#    img = preprocess.bounding_word(preprocess.do2(filename))
    img = preprocess.bounding_letter(preprocess.process_text(filename))
    return
