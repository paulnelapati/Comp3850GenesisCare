# Comp3850GenesisCare - Medicine Box Reader
Read the important information from a given picture

# Installation
clone the repo to any location
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
Currently performs at 33-47% success rate

## Drawbacks
Can not yet handle images with multiple boxes
can not handle rotated, flipped, or other odd orientations