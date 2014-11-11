##
## bounding.py for  in /home/pprost
## 
## Made by  Prost P.
## Login   <pprost@epitech.net>
## 
## Started on  Tue Nov 11 20:42:30 2014 Prost P.
## Last update Tue Nov 11 21:44:08 2014 Prost P.
##

import cv2
import do

def bounding(img):
    contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    idx =0
    img = do.threshold(img)
    for cnt in contours:
        idx += 1
        x,y,w,h = cv2.boundingRect(cnt)
        roi = img[y:y + h, x:x + w]
#        cv2.imwrite(str(idx) + '.jpg', roi)

        cv2.rectangle(img ,(x,y), (x+w,y+h), (200,150,0), 1)
    cv2.imshow('bounding detection', img)
    cv2.waitKey(0)
    return img

