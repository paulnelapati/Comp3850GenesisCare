# -*- coding: utf-8 -*-
"""
Created on Sun May  2 15:21:46 2021

@author: Lachlan
"""

###################################

import cv2
import numpy as np
import pytesseract
import os
import time
import re
import ProcessingElements as PE

###################################

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
inputPath = "./input/"
inputType = ["png", "jpg", "jpeg"]
testPath='./testcases/'
outputPath='./output/'
outputType='.csv'           # .txt or .csv supported
debuggingPath=outputPath+'Result_'+timestr+"/"
imageWidthLim = [400, 800]  # max should be 2xmin+
debugging = False           #enable view and save of intermediary images and text

###################################

start = time.time()

#retrieves the name of the newest .csv in the output folder
def importResult():
    arr = os.listdir(outputPath)
    # print(arr)
    fileList = []
    for a in arr:
        if (re.match(".+("+outputType+")$",a)):
            fileList.append(a)
    return fileList[len(fileList)-1]

#retrieves the list of test cases in the testcase folder
#currently only returns the first file it finds
def importTestCase():
    arr = os.listdir(testPath)
    # print(arr)
    fileList = []
    for a in arr:
        if (re.match("(TestCase).+("+outputType+")$",a)):
            fileList.append(a)
    return fileList[0]

#loop over the output result and the testcase arrays 
#element by element compare them using regex (if either is a subset of the other)
#use regex to remove single brackets and other grammar that can break regex statements
#return the percentage of times a match was found 
def calculateAccuracy(Result, Testcase):
    count = 0
    total = 0
    print("i, j, Result, r, t:  i j Result Processed Testcase")
    for i in range(len(Result)):
        #ignore row/col 0 as they are headers
        if (i==0):
            continue
        for j in range(len(Result[i])):
            if (j==0):
                print("\n"+Result[i][j])
                continue
            #have only 0 brackets or a bracket pair
            process = re.search(r"(\w+|/|\-| )*(\((\w+|/|\-| )*\))*(\w+|/|\-| )*", Result[i][j])
            # process2 = re.search("(\w+|/|\-| )*(\((\w+|/|\-| )*\))*(\w+|/|\-| )*", Result[i][j])
            # if(process2):
            #     print("\nbrackets: ", process2)
            r = process[0]
            # r = re.escape(Result[i][j])
            # t = re.escape(Testcase[i][j])
            # r = (Result[i][j])
            t = Testcase[i][j]
            # print("i, j, Result, r, t: ", i, j, Result[i][j], r, t)
            #remove spaces and other annoyign characters
            R = re.sub("[^a-zA-Z0-9\-\/\(\)]","", r)
            T = re.sub("[^a-zA-Z0-9\-\/\(\)]","", t)
            print("i, j, Result, r, t: ", i, j, Result[i][j], R, T)
            # print (re.match(".*"+r+".*",t), re.match(".*"+t+".*",r))
            
            total = total + 1
            if (re.match(".*"+R+".*",T) or re.match(".*"+T+".*",R)):
                count = count + 1
                print("count, total: ", count, total)
    if (count==0):  
        return 0
    return round(count/total*100, 2)

#run the main program
PE.runProgram()

#import the data and calculate the accuracy
arr1 = importResult()
Result = np.loadtxt(outputPath+arr1, dtype = 'str', delimiter = ",")
arr2 = importTestCase()
Testcase = np.loadtxt(testPath+arr2, dtype = 'str', delimiter = ",")
# print (arr1)
# print (arr2)
# print (Result)
# print (Testcase)
accuracy = calculateAccuracy(Result, Testcase)
print("\naccuracy: "+str(accuracy)+"%")

#print the time the system took to run
end = time.time()
print ("Testtime: "+ str(round(end-start)) + " seconds")

