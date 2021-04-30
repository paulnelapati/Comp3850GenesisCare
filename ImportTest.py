# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 17:27:51 2021

@author: Lachlan
"""

import cv2
import numpy as np
# import pytesseract
import os
import time
import re
timestr = time.strftime("%Y-%m-%d_%H-%M-%S")

# https://accesspharmacy.mhmedical.com/content.aspx?bookid=1549&sectionid=93411751
# https://pharmafactz.com/medicine-prefixes-and-suffixes/


MedicalNames = np.loadtxt("./MedicalWords.csv", dtype = 'str', delimiter = ",")
ChemicalBlock ="Amlodipine"
for n in MedicalNames:
    ChemicalBlock = ChemicalBlock+"|"+n
print (ChemicalBlock)
ChemicalRegex = ".*("+ChemicalBlock+").*"
print (ChemicalRegex)





#np.savetxt(outputPath+"Name"+"_"+timestr+outputType,wordLists, fmt = '%-1s', delimiter=",")
#np.savetxt(outputPath+"Name.csv",wordLists, fmt = '%-1s', delimiter=",")
# for n in MedicalNames:
    # print (n)

# print(MedicalNames)

