import cv2
import sift
import surf
import sys

def main():
	img = cv2.imread(sys.argv[1])
	gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	chr = sift.getCharacter(gray)
	print chr
	chr = surf.getCharacter(gray)
	print chr

if __name__ == '__main__':
	main()
