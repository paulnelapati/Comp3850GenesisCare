# -*- coding: utf-8 -*-
"""
Created on Tue May 18 12:00:07 2021

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
import sys

###################################
if sys.platform == 'Windows':
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

#run the main program
PE.runProgram()
