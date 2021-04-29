# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 23:20:56 2021

@author: Lachlan
"""

import cv2
import numpy as np
import pytesseract
import os
import time
import re
timestr = time.strftime("%Y-%m-%d_%H-%M-%S")

#from matplotlib import pyplot as plt
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
inputPath = "./input/"
outputPath='./output/'
outputType='.csv' # .txt or .csv supported

def importPics():
    arr = os.listdir(inputPath)
    print(arr)
    fileList = []
    for a in arr:
        if (re.match(".+\.(png|jpg|jpeg)$",a)):
            fileList.append(a)
    return fileList

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def labelImage(img, colour, text, boxes, scale):
    wordList = []
    for x,b in enumerate(boxes.splitlines()):
        if x!=0:
            b = b.split()
            if len(b)==12:
                x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255),scale)
                if (text):
                    cv2.putText(img,b[11],(x,y+40),cv2.FONT_HERSHEY_COMPLEX,0.5,(50,50,255),scale)
                wordList.append(b[11])
    #print(wordList)
    return wordList

def genOptions(names):
    wordLists = []
    for name in names:
        img = cv2.imread(inputPath+name)
        # img = cv2.GaussianBlur(img,(7,7),0)
        edges = cv2.Canny(img,100,200)
        #edges = cv2.GaussianBlur(edges,(5,5),0)
        edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2RGB)
        invedges = cv2.bitwise_not(edges)

        print(name)
        
        #whiteback edges
        wordList = genOption(name, invedges, False, False, 1, 4)
        wordLists.append(wordList)
        # genOption(name, invedges, False, False, 4, 4)
        # genOption(name, invedges, False, False, 8, 4)
        # genOption(name, invedges, False, False, 16, 5)
        
        #blackback edges
        wordList = genOption(name, edges, False, False, 1, 3)
        wordLists.append(wordList)
        # genOption(name, edges, False, False, 4, 3)
        # genOption(name, edges, False, False, 8, 3)
        # genOption(name, edges, False, False, 16, 3)
        
        #colour
        wordList = genOption(name, img, True, False, 1, 1)
        wordLists.append(wordList)
        # genOption(name, img, True, False, 4, 1)
        # genOption(name, img, True, False, 8, 1)
        # genOption(name, img, True, False, 16, 1)
        
        #greyscale
        wordList = genOption(name, img, False, False, 1, 2)
        wordLists.append(wordList)
        # genOption(name, img, False, False, 4, 2)
        # genOption(name, img, False, False, 8, 2)
        # genOption(name, img, False, False, 16, 2)
        
        #inverted, not running :
        # genOption(name, img, True, True, 1, 3)
        # genOption(name, img, True, True, 4, 3)
        # genOption(name, img, False, True, 1, 4)
        # genOption(name, img, False, True, 4, 4)
    return wordLists

def genOption(name, img, colour, invert, scale, idNumber):
    if (colour):
        img1 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        print(name + " colour")
        #print(img1)
    else:
        img1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        print(name + " grey")
        #print(img1)
    if (invert):
        img1 = cv2.bitwise_not(img1)
    if (scale!=1):
        w,h,c = img.shape
        img1 = cv2.resize(img1,(int(h*scale),int(w*scale)))
        boxes = pytesseract.image_to_data(img1)
        if (colour==False):
            img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2RGB)
        wordList = labelImage(img1, colour, False, boxes, scale)
        img1 = cv2.resize(img1,(h,w))
        cv2.imshow('Result ' +str(idNumber)+'_'+str(scale)+'xS '+name,img1)
        return wordList
    else:
        boxes = pytesseract.image_to_data(img1)
        if (colour==False):
            img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2RGB)
        wordList = labelImage(img1, colour, False, boxes, scale)
        cv2.imshow('Result ' +str(idNumber)+' '+name,img1)
        return wordList


names = importPics()
wordLists = genOptions(names)
print(wordLists)
np.savetxt(outputPath+"Name"+"_"+timestr+outputType,wordLists, fmt = '%-1s', delimiter=",")
#np.savetxt(outputPath+"Name.csv",wordLists, fmt = '%-1s', delimiter=",")
cv2.waitKey(0)
cv2.destroyAllWindows()
    

