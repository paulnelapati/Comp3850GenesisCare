# Comp3850GenesisCare - Medicine Box Reader
This project is designed to produce a table of results to summarise the important information from a given picture of a medication box including:
1. Brand Name
2. Active Ingredient
3. Concentration/Dosage
4. Quantity In Box

# Installation
Clone the repo to any location  
git clone https://github.com/LachlanMatt/Comp3850GenesisCare

## Requirements
Need to install 
* Cv2 
* Numpy 
* Pytesseract
* Google Teseract at (confiurable):
    * C:\Program Files\Tesseract-OCR\tesseract.exe

## Usage
Steps to use:
1. Place target images in the input folder (configuable):
    * ./input
2. Run RunDetection 
3. Output will be Reult_date_time.csv in the output folder (configurable):
    * ./output

# Performance Limitations
Version 0.5

## Success
Currently performs at 33-47% success rate on results 2-4 (excluding brand name) for a given testset of reasonable images (correct orientation, angle, resolution).

## Drawbacks
Can not yet handle images with multiple boxes.  
Can not handle rotated, flipped, or other odd orientations.  
Performs poorly on low resolution images.  
Only tested on Windows, Docker implementation pending.  
