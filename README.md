# Comp3850GenesisCare - Medicine Box Reader
This project is designed to produce a table of results to summarise the important information from a given picture of a medication box including:
1. Brand Name
2. Active Ingredient
3. Concentration/Dosage
4. Quantity In Box  
The purpose of this is to automate the process of acquiring user medical records to save time for medical staff and increase the opporational efficiency of the business

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

## Format
Input:
* Allowed file types (configurable) are .jpg, .jpeg, and .png; Other files will be ignored

Output:
* Formatted .csv file
* Top row is headings, describing the field below
* Left column is the name of the file the data came from
* Undetermined data filled with "-"

Testcases:
* Same format as Output
## Usage
Steps to use:
1. Place target images in the input folder (configuable):
    * ./input/
2. (Optional) Enable Debugging=True in ProcessingElements.py to have intermediary data saved to (configurable):
    * ./output/Result_date_time/
3. Run RunDetection.py 
4. Output will be Reult_date_time.csv in the output folder (configurable):
    * ./output/


## Testing
Steps to test:
1. Put testcase images and expected output in their relevant folders (configurable):
    * Input images: ./input/
    * Expected output: ./testcases/
2. Run PerformanceTest.py

# Performance
For Version 0.5

## Features
Current:
* Can detect the important text from simple images
Planned:
* Can use a document scanner function to detect text in difficult images
* Utilise Docker to allow for easy devloyment

## Success
Currently performs at 33-47% success rate on results 2-4 (excluding brand name) for a given testset of reasonable images (correct orientation, angle, resolution).

## Drawbacks
* Can not yet handle images with multiple boxes.  
* Can not handle rotated, flipped, or other odd orientations.  
* Performs poorly on low resolution images.  
* Only tested on Windows, Docker implementation pending.  
