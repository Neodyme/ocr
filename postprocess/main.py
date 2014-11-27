import cv2
from postprocess import postprocess
import sys

def main():
	img = cv2.imread(sys.argv[1])
	gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	p = postprocess()
	# chr = p.sift(gray)
	# print chr
	# chr = p.surf(gray)
	# print chr
	# chr = p.sift(gray)
	# print chr
	# chr = p.surf(gray)
	# print chr
	# chr = p.sift(gray)
	# print chr
	# chr = p.surf(gray)
	# print chr
	# chr = p.sift(gray)
	# print chr
	# chr = p.surf(gray)
	# print chr
	# chr = p.sift(gray)
	# print chr
	# chr = p.surf(gray)
	# print chr
	# chr = sift.getCharacter(gray)
	# print chr
	# chr = surf.getCharacter(gray)
	# print chr


if __name__ == '__main__':
	main()
