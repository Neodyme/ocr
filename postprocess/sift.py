import cv2
import numpy as np
import glob
import os
import sys
import operator
sys.path.insert(0, './')
from preprocess import do

path = "./example_dataset/step1/"

strtochrsym = {
    "amper": "&",
    "apos": "'",
    "arob": "@",
    "bquote": "`",
    "bslash": "\\",
    "caret": "^",
    "colon": ":",
    "comma": ",",
    "dollar": "$",
    "equal": "=",
    "exclmark": "!",
    "gthan": ">",
    "hyphen": "-",
    "lcbracket": "{",
    "lparen": "(",
    "lsqbracket": "[",
    "lthan": "<",
    "num": "#",
    "pcent": "%",
    "pipe": "|",
    "plus": "+",
    "point": ".",
    "questmark": "?",
    "quotmark": "\"",
    "rcbracket": "}",
    "rparen": ")",
    "rsqbracket": "]",
    "scolon": ";",
    "slash": "/",
    "space": " ",
    "star": "*",
    "tilde": "~",
    "under": "_"
}

def calculate(img1, img2):
    detector = cv2.SIFT()

    # # detect keypoints
    kp1 = detector.detect(img1, None)
    kp2 = detector.detect(img2, None)

    # descriptors
    k1, d1 = detector.compute(img1, kp1)
    k2, d2 = detector.compute(img2, kp2)
    if d2 == None:
        return 0
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    # Match descriptors.
    matches = bf.match(d1,d2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)

    val = 0.0
    for matche in matches:
        val += matche.distance
    if (len(matches) > 0):
        val /= len(matches)

    val = (1 - (val / 1000)) * 100.0

    return val

def getAllImageData():
    collect = {}
    for f in glob.glob("*.bmp"):
        tmp = f.split('.')
        pos = tmp[0].find("_small", 0)
        c = ""
        if pos < 0:
            pos = tmp[0].find("sym_", 0)
            if pos >= 0:
                c = strtochrsym[tmp[0][pos+4:]]
            else:
                pos = tmp[0].find("num_", 0)
                if pos >= 0:
                    c = tmp[0][pos+4:]
                else:
                    c = tmp[0].upper()
        else:
            c = tmp[0][:pos]
        collect[c] = f
    return collect

def getCharacter(img):
    old_path = os.getcwd()
    os.chdir(path)
    db = getAllImageData()
    best = {}
    for key, value in db.items():
        tmp = cv2.imread(value)
        gray= cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY)
        s = calculate(img, gray)
        best[s] = key
    os.chdir(old_path)
    sorted_best = sorted(best.items(), key=operator.itemgetter(0))
    best = list(reversed(sorted_best))
    ret = best[:5]
    if (len(ret) < 5):
        return []
    return ret
