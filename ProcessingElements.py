# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 23:20:56 2021

@author: Lachlan Matthews
"""

###################################

import cv2
import numpy as np
import pytesseract
import os
import time
import re


###################################

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
inputPath = "./input/"
inputType = ["png", "jpg", "jpeg"]
testPath='./testcases/'
outputPath='./output/'
outputType='.csv'           # .txt or .csv supported
debuggingPath=outputPath+'Result_'+timestr+"/"
imageWidthLim = [400, 800]  # Max should be 2xMin+
debugging = False           #enable view and save of intermediary images and text

###################################

# structure:
# main
#   genRegex
#   importPics
#   processImages
#       detectText
#           labelImage
#       processText
#           bestAnswer

# ChemicalRegex = genChemicalRegex()
# QuantityRegex = genQuantityRegex()
# UnitsRegex = genUnitsRegex()

#main function
def runProgram():
    if (debugging):
        start = time.time()
        os.mkdir(debuggingPath)
    RegexStrings = genRegex()
    names = importPics()
    answerList = processImages(names, RegexStrings)
    print(answerList)
    np.savetxt(outputPath+"Result_"+timestr+outputType,answerList, fmt = '%-1s', delimiter=",")
    #np.savetxt(outputPath+"Name.csv",wordLists, fmt = '%-1s', delimiter=",")
    if (debugging):
        end = time.time()
        print ("Runtime: "+ str(round(end-start)) + " seconds")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

#generats a dictionary contain strings or string arrays 
#they are used to process the raw text into formatted text
def genRegex():
    RegexStrings = {
        "ChemicalRegex": genChemicalRegex(),
        "QuantityRegex": genQuantityRegex(),
        "UnitsRegex": genUnitsRegex()
    }
    return RegexStrings

#the chemical name (active ingredient) is from a csv file 
#that is able to be edited/added to independantly from this file
def genChemicalRegex():
    MedicalNames = np.loadtxt("./MedicalWords.csv", dtype = 'str', delimiter = ",")
    ChemicalBlock ="Amlodipine"
    for n in MedicalNames:
        ChemicalBlock = ChemicalBlock+"|"+n
    ChemicalRegex = ".*("+ChemicalBlock+").*"
    return ChemicalRegex
    
#[0] detect keyword associated with value
#[1] guarantee it's a number with no capital Oh's instead of zero's
def genQuantityRegex():
    QuantityRegex = ["(.*(tablet|capsule|sachet).*)|(x)" , ".*[0-9]+[^O].*"]
    return QuantityRegex

#[0] detect keyword associated with value
#[1] guarantee it's a number with no capital Oh's instead of zero's
def genUnitsRegex():
    UnitsRegex =[ "(.*(mg).*)|(g)", ".*[0-9]+[^O].*"]
    return UnitsRegex
   
#get a list of file names of the correct 
#file type from the configured input folder
def importPics():
    arr = os.listdir(inputPath)
    # print(arr)
    fileList = []
    fileType = inputType[0]
    for t in inputType:
        fileType = fileType+"|"+t
    for a in arr:
        if (re.match(".+\.("+fileType+")$",a)):
            fileList.append(a)
    return fileList

#resize the images to be roughly similar in size
#send to image pre-processing to generate augmented images and raw text
#raw text is sent to text processor
#return formatted text array
def processImages(names, RegexStrings):
    wordLists = []
    answerList = [["Filename", "Chemical", "Units", "Quanity"]]
    imageWidthLim[1] = max(imageWidthLim[1], imageWidthLim[0]*2)
    for file in names:
        img = cv2.imread(inputPath+file)
        while (img.shape[0]>imageWidthLim[1]):
            img = cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))
        while (img.shape[0]<imageWidthLim[0]):
            img = cv2.resize(img,(int(img.shape[1]*2),int(img.shape[0]*2)))
        
        # img = cv2.GaussianBlur(img,(7,7),0)
        edges = cv2.Canny(img,100,200)
        #edges = cv2.GaussianBlur(edges,(5,5),0)
        edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2RGB)
        invedges = cv2.bitwise_not(edges)
        print("\n"+file)
        
        name = file.split('.')[0]
        localWordList = []
        #whiteback edges
        wordList = detectText(name, invedges, False, False, 1, 1)
        wordLists.append(wordList)
        localWordList.append(wordList)
        
        #blackback edges
        wordList = detectText(name, edges, False, False, 1, 2)
        wordLists.append(wordList)
        localWordList.append(wordList)
        
        #colour
        wordList = detectText(name, img, True, False, 1, 3)
        wordLists.append(wordList)
        localWordList.append(wordList)
        
        #greyscale
        wordList = detectText(name, img, False, False, 1, 4)
        wordLists.append(wordList)
        localWordList.append(wordList)
        
        #inverted, not running :
        # wordList = detectText(name, img, True, True, 1, 5)
        # wordLists.append(wordList)
        # localWordList.append(wordList)
        
        bestAnswer = processText(localWordList,name, RegexStrings)
        answerList.append(bestAnswer)
        
    return answerList

#augmented images have pre-processing stages applied
#text in images is detected
#these images are sent to have text lebelled
#return raw text
def detectText(name, img, colour, invert, scale, idNumber):
    if (colour):
        img1 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        # print(name + " colour")
        #print(img1)
    else:
        img1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # print(name + " grey")
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
        if (debugging):
            cv2.imshow('Result ' +str(idNumber)+'_'+str(scale)+'xS '+name,img1)
            cv2.imwrite(debuggingPath + name + " " + str(idNumber)+".png", img1)
        return wordList
    else:
        boxes = pytesseract.image_to_data(img1)
        if (colour==False):
            img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2RGB)
        wordList = labelImage(img1, colour, False, boxes, scale)
        if (debugging):
            cv2.imshow('Result ' +str(idNumber)+' '+name,img1)
            cv2.imwrite(debuggingPath + name + " " + str(idNumber)+".png", img1)
        return wordList

#images are labelled and raw text array is generated
#return raw text
def labelImage(img, colour, text, boxes, scale):
    wordList = []
    for x,b in enumerate(boxes.splitlines()):
        if x!=0:
            b = b.split()
            if len(b)==12:
                if (debugging):
                    x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                    cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255),scale)
                    if (text):
                        cv2.putText(img,b[11],(x,y+40),cv2.FONT_HERSHEY_COMPLEX,0.5,(50,50,255),scale)
                wordList.append(b[11])
    #print(wordList)
    return wordList

#raw text is inputted, and using regex a processed array is produced
#return processed text
def processText(localWordList,name, RegexStrings):

    ChemicalRegex = RegexStrings["ChemicalRegex"]
    QuantityRegex = RegexStrings["QuantityRegex"]
    UnitsRegex = RegexStrings["UnitsRegex"]

    ChemicalResults = []
    UnitsResults = []
    QuantityResults = []
    
    for List in localWordList:
        i = 0
        for word in List:
            if (re.match(ChemicalRegex,word) and word not in ChemicalResults):
                ChemicalResults.append(List[i])
            if (re.match(UnitsRegex[0],word) and word not in UnitsResults):
                phrase = List[i-1] +" "+ List[i]
                if (re.match(UnitsRegex[1],phrase) and phrase not in UnitsResults):
                    UnitsResults.append(phrase)
            if (re.match(QuantityRegex[0],word) and word not in QuantityResults):
                phrase = List[i-1] +" "+ List[i]
                if (re.match(QuantityRegex[1],phrase) and phrase not in QuantityResults):
                    QuantityResults.append(List[i-1] +" "+ List[i])
            i = i+1
            
    print("ChemicalResults", ChemicalResults)
    print("UnitsResults", UnitsResults)
    print("QuantityResults", QuantityResults)
    
    if (debugging):
        np.savetxt(debuggingPath+name+" RawText"+outputType,localWordList, fmt = '%-1s', delimiter=",")
        np.savetxt(debuggingPath+name+" ChemicalResults"+outputType,ChemicalResults, fmt = '%-1s', delimiter=",")
        np.savetxt(debuggingPath+name+" UnitsResults"+outputType,UnitsResults, fmt = '%-1s', delimiter=",")
        np.savetxt(debuggingPath+name+" QuantityResults"+outputType,QuantityResults, fmt = '%-1s', delimiter=",")

    ChemicalAnswer  = bestChemicalAnswer(ChemicalResults)
    UnitsAnswer     = bestUnitsAnswer(UnitsResults)
    QuantityAnswer  = bestQuantityAnswer(QuantityResults)
    bestAnswer = [name, ChemicalAnswer, UnitsAnswer, QuantityAnswer]
    return bestAnswer

#given a list of possible answers, the best is picked
#currently picks first, advanced functionality is unimplemented
#if list is empty, return - (empty lists have no [0])
def bestChemicalAnswer(ChemicalResults):
    if (len(ChemicalResults) >0):
        return ChemicalResults[0]
    else:
        return "-"
    
def bestUnitsAnswer(UnitsResults):
    if (len(UnitsResults) >0):
        return UnitsResults[0]
    else:
        return "-"
    
def bestQuantityAnswer(QuantityResults):
    if (len(QuantityResults) >0):
        return QuantityResults[0]
    else:
        return "-"
  
#run program by using the test file or the run file, 
#not the elements file    
# runProgram()

    
