import cv2
import numpy as np
import glob
import os
import sys
import operator
sys.path.insert(0, './')
from preprocess import do

path = "./dataset/"

# strtochrsym = {
#     "amper": "&",
#     "apos": "'",
#     "arob": "@",
#     "bquote": "`",
#     "bslash": "\\",
#     "caret": "^",
#     "colon": ":",
#     "comma": ",",
#     "dollar": "$",
#     "equal": "=",
#     "exclmark": "!",
#     "gthan": ">",
#     "hyphen": "-",
#     "lcbracket": "{",
#     "lparen": "(",
#     "lsqbracket": "[",
#     "lthan": "<",
#     "num": "#",
#     "pcent": "%",
#     "pipe": "|",
#     "plus": "+",
#     "point": ".",
#     "questmark": "?",
#     "quotmark": "\"",
#     "rcbracket": "}",
#     "rparen": ")",
#     "rsqbracket": "]",
#     "scolon": ";",
#     "slash": "/",
#     "space": " ",
#     "star": "*",
#     "tilde": "~",
#     "under": "_"
# }

class postprocess:
    def __init__(self):
        old_path = os.getcwd()
        os.chdir(path)
        self.libSift = {}
        self.libSurf = {}
        db = self.getAllImageData()
        for key, value in db.items():
            tmp = cv2.imread(value)
            gray= cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY)
            self.libSift[key] = self.calculate(gray, cv2.SIFT)
            self.libSurf[key] = self.calculate(gray, cv2.SURF)

        os.chdir(old_path)

    def calculate(self, img, algo):
        detector = algo()
        kp = detector.detect(img, None)
        k, d = detector.compute(img, kp)
        if d == None:
            return None
        return d

    def match(self, img, d2, algo):
        detector = algo()

        # # detect keypoints
        kp1 = detector.detect(img, None)

        # descriptors
        k1, d1 = detector.compute(img, kp1)
        if d1 == None or d2 == None:
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
        if algo == cv2.SIFT:
            val = (1 - (val / 1000)) * 100.0
        else:
            val = (1 - val) * 100.0
        return val

    def getAllImageData(self):
        collect = {}
        for f in glob.glob("*.bmp"):
            tmp = f.split('.')
            collect[tmp[0]] = f
        return collect

    def getCharacter(self, img, algo):
        best = {}
        if algo == cv2.SIFT:
            lib = self.libSift
        else:
            lib = self.libSurf

        for key, value in lib.items():
            s = self.match(img, value, algo)
            if key[0] in best.keys():
                if s > best[key[0]]:
                    best[key[0]] = s
            else:
                best[key[0]] = s
        sorted_best = sorted(best.items(), key=lambda x: x[1])
        best = list(reversed(sorted_best))
        ret = best[:5]
        if (len(ret) < 5):
            return []
        return ret

    def sift(self, img):
        return self.getCharacter(img, cv2.SIFT)

    def surf(self, img):
        return self.getCharacter(img, cv2.SURF)
