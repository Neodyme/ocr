import cv2
import numpy as np
import glob
import os
import sys
sys.path.insert(0, '../')
from preprocess import do

path = "../example_dataset/step1/"

def calculate(img1, img2):
	hessian_threshold = 5000
	detector = cv2.SURF(hessian_threshold)
	# # Initiate STAR detector
	# star = cv2.FeatureDetector_create("SURF")

	# # Initiate BRIEF extractor
	# brief = cv2.DescriptorExtractor_create("SURF")

	# # detect keypoints
	# kp1 = star.detect(img1)
	# kp2 = star.detect(img2)

	# descriptors
	k1, d1 = detector.detectAndCompute(img1, None)
	k2, d2 = detector.detectAndCompute(img2, None)
	print d2
	# create BFMatcher object
	bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

	# Match descriptors.
	matches = bf.match(d1,d2)

	# Sort them in the order of their distance.
	matches = sorted(matches, key = lambda x:x.distance)

	val = 0.0
	for matche in matches:
		val += matche.distance
	val /= len(matches)
	val = (1.0 - val) * 100.0

	return val

def getAllImageData():
	os.chdir(path)
	collect = {}
	for f in glob.glob("*.bmp"):
		tmp = f.split('.')
		pos = tmp[0].find("_small", 0)
		c = ""
		if pos < 0:
			pos = tmp[0].find("sym_", 0)
			if pos >= 0:
				c = tmp[0][pos+4:]
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
	db = getAllImageData()
	best = ""
	score = 0.0
	for key, value in db.items():
		if len(key) != 1:
			continue
		print key
		tmp = do.do(value)
		s = calculate(img, tmp)
		if s > score:
			score = s
			best = key
	return best
