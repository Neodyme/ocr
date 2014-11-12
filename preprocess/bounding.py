##
## bounding.py for  in /home/pprost
## 
## Made by  Prost P.
## Login   <pprost@epitech.net>
## 
## Started on  Tue Nov 11 20:42:30 2014 Prost P.
## Last update Wed Nov 12 01:08:18 2014 Prost P.
##

import cv2
import do

def bounding(img):
    contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    idx = 0
    img2 = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    box = []
    for cnt in contours:
        box.append(cv2.boundingRect(cnt))

#
# premiere passe
    gr = []
    used = []
    for b in box:
        if b[0] < 10:
            continue
        if b in used:
            for n in gr:
                if b in n:
                    break
        else:
            n = [b]
            gr.append(n)
        for a in box:
            if (abs(b[0] - (a[0] + a[2])) < 5 or abs(a[0] - (b[0] + b[2])) < 5)\
               and abs((a[1] + a[3] / 2) - b[1] + b[3] / 2) < 10:
                n.append(a)
                used.append(a)
        used.append(b)

#
# deuxieme passe

    gr2 = []
    for n in gr:
        gr2.append([min([x[0] for x in n]),
                    min([x[1] for x in n]),
                    max([x[0] + x[2] for x in n]),
                    max([x[1] + x[3] for x in n])])
        

    gr = []
    used = []
    for b in gr2:
        if b in used:
            for n in gr:
                if b in n:
                    break
        else:
            n = [b]
            gr.append(n)
        for a in gr2:
            if ((abs(b[0] - (a[2])) < 7 or abs(a[0] - (b[2])) < 7)\
                and abs((a[1] + (a[3] - a[1]) / 2) - (b[1] + (b[3] - b[1]) / 2)) < 5) or\
\
             (((a[0] >= b[0]) and (a[1] >= b[1]) and (a[2] <= b[2]) and (a[3] <= b[3])) and b[0] > 10) or\
\
            ((a[0] <= b[0]) and (a[1] <= b[1]) and (a[2] >= b[2]) and (a[3] >= b[3]) and a[0] > 10) or\
\
            ((((a[2] >= b[0]) and (a[2] <= b[2]) and (a[0] <= b[0])) or\
              ((a[0] <= b[2]) and (a[0] >= b[0]) and (a[2] >= b[2]))) and \
             (abs((a[1] + (a[3] - a[1]) / 2) - (b[1] + (b[3] - b[1]) / 2)) < 5)):
                n.append(a)
                used.append(a)

        used.append(b)

    for n in gr:
        gxmin = min([x[0] for x in n])
        gymin = min([x[1] for x in n])
        gwmax = max([x[2] for x in n])
        ghmax = max([x[3] for x in n])
        cv2.rectangle(img2,(gxmin, gymin),(gwmax,ghmax),(200,0,0),1)
#        print(n)
        
            #         roi = img[y:y + h, x:x + w]
#    print(gr)
    cv2.imshow('bounding detection', img2)
    cv2.waitKey(0)
    return img

