import cv2
import surf
import sys

def main():
	img = cv2.imread(sys.argv[1])
	gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	surf.getCharacter(gray)

if __name__ == '__main__':
	main()