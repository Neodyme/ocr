##
## bounding.py for  in /home/pprost
## 
## Made by  Prost P.
## Login   <pprost@epitech.net>
## 
## Started on  Tue Nov 11 20:42:30 2014 Prost P.
## Last update Tue Nov 25 21:03:09 2014 Prost P.
##

#        for i in range(0, len(contours)):
#            if :
#                test = True
#                break

import cv2
import do

def checkPointInBox(x, y, box):
    if x >= box[0] and x <= box[0] + box[2] and y >= box[1] and y <= box[1] + box[3]:
        return True
    return False

def doesOtherBoxCross(box, otherBox):
        if checkPointInBox(otherBox[0], otherBox[1], box) or \
           checkPointInBox(otherBox[0] + otherBox[2], otherBox[1], box) or \
           checkPointInBox(otherBox[0], otherBox[1] + otherBox[3], box) or \
           checkPointInBox(otherBox[0] + otherBox[2], otherBox[1] + otherBox[3], box):
            return True
        return False


def clean_image(img, box, listBox):
    i = 0
    for otherBox in listBox:
        if otherBox[0] == box[0] and otherBox[1] == box[1] and otherBox[2] == box[2] and otherBox[3] == box[3] or \
           doesOtherBoxCross(box, otherBox) == False:
            continue
        cleanX = box[0] - otherBox[0]
        for x in range(max(otherBox[0] - box[0], 0), min((otherBox[0] + otherBox[2]) - box[0], box[2])):
            for y in range(max(otherBox[1] - box[1], 0), min((otherBox[1] + otherBox[3]) - box[1], box[3])):
                img[y][x] = 255
        i += 1
    return img

def sortListBox(listBox):
    return sorted(listBox, key=lambda box:((box[0] + box[0] + box[2]) / 2))

def bounding_letter(img):
    print("test")
    contours,hierarchy = cv2.findContours(do.threshold(img.copy()),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#    print(contours)
    img2 = img.copy()
    img3 = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    letter = []
    retBox = []
#    print(hierarchy)
    for i in range(0, len(contours) - 1):
        if hierarchy[0][i][3] != 0 and hierarchy[0][i][2] == -1:
            continue
#        cv2.drawContours(img2, contours, i, (0,0,0), 3)
        box = cv2.boundingRect(cv2.approxPolyDP(contours[i], 3, True))
        retBox.append(box)
        #        print(letter[len(letter) - 1])
        #        cv2.imshow('letter bounding detection', letter[len(letter) - 1])
        #        cv2.waitKey(0)
        #    print(box)
        retBox = sortListBox(retBox)
    for box in retBox:
        letter.append(clean_image(img2.copy()[box[1]:(box[1] + box[3]), box[0]:(box[0] + box[2])], box, retBox))
#        cv2.rectangle(img2, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0,0,200),1)
        cv2.rectangle(img3, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0,0,200),1)
 #       cv2.imshow('end letter bounding detection', img3)
#        cv2.waitKey(0)

 #   for let in letter:
  #      cv2.imshow('2end letter bounding detection', let)
   #     cv2.waitKey(0)

    return letter, retBox

def bounding_word(img, filename):
    img3 = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    contours, hierarchy = cv2.findContours(do.threshold(img.copy()), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
               and (b[1] <= a[1] + a[3] and b[1] >= a[1] or \
                    b[1] + b[3] <= a[1] + a[3] and b[1] + b[3] >= a[1]):
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
             (((a[0] >= b[0]) and (a[1] >= b[1]) and (a[2] <= b[2]) and (a[3] <= b[3])) and b[0] > 10) or\
             ((a[0] <= b[0]) and (a[1] <= b[1]) and (a[2] >= b[2]) and (a[3] >= b[3]) and a[0] > 10) or\
             ((((a[2] >= b[0]) and (a[2] <= b[2]) and (a[0] <= b[0])) or\
             ((a[0] <= b[2]) and (a[0] >= b[0]) and (a[2] >= b[2]))) and \
             (abs((a[1] + (a[3] - a[1]) / 2) - (b[1] + (b[3] - b[1]) / 2)) < 5)):
                n.append(a)
                used.append(a)
        used.append(b)


    ret = []
    ret2 = []
    for n in gr:
        gxmin = min([x[0] for x in n])
        gymin = min([x[1] for x in n])
        gwmax = max([x[2] for x in n])
        ghmax = max([x[3] for x in n])
        cv2.rectangle(img2,(gxmin, gymin),(gwmax,ghmax),(200,0,0),1)
        ret.append([gxmin, gymin, gwmax, ghmax, True])

#
# 3e passe, detection de ligne et ordinance des mots
    phrases = []
    used = []
    for b in ret:
        if b[0] < 10:
            continue
        if b in used:
            for n in gr:
                if b in n:
                    break
        else:
            n = [b]
            phrases.append(n)
        for a in ret:
             gymin = min([x[1] for x in n])             
             ghmax = max([x[3] for x in n])
             if (b[1] <= a[3] and b[1] >= a[1] or \
                b[3] <= a[3] and b[3] >= a[1]) and abs(((ghmax - gymin)/2) - ((a[3] - a[1]) / 2)) < 30 :
                n.append(a)
                used.append(a)
        used.append(b)

#
# tri
#
    phrases.sort(key=lambda x: min([key[1] for key in x]))
    j = 0
    ret = []
    for n in phrases:
        gxmin = min([x[0] for x in n])
        gymin = min([x[1] for x in n])
        gwmax = max([x[2] for x in n])
        ghmax = max([x[3] for x in n])
        
        n.sort(key=lambda x: x[0])

        cv2.putText(img2, "{}".format(j), (gxmin - 30, gymin),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (0, 200, 100))
        k = 0
        for i in n:
            for n2 in phrases:
                if len(n2) == 0:
                    phrases.remove(n2)
                if i in n2 and n2 != n:
                    n2.remove(i)
                cv2.putText(img2, "{}".format(k), (i[0], i[1]),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (0, 0, 255))
                k += 1
            cv2.rectangle(img2,(gxmin, gymin),(gwmax,ghmax),(50,200,40),1)
        return_phrase = ([img3[(x[1] - 2):(x[3] + 2), (x[0] - 2):(x[2] + 2)].copy() for x in n])
        ret.append(return_phrase)
        j += 1


    cv2.imshow('test word bounding detection', img2)
    cv2.waitKey(0)
    return ret

