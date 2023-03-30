import numpy as np
import cv2
import os
from PIL import Image

# rectangle height and width
rectWt = 118
rectHt = 118

# defining path to run local data
brainScansPath = "C:/Users/divya/OneDrive/Desktop/DM/PatientData-1/PatientData/Data"

def getSlices(pic, picInGray, attributes, rectangleWt, rectangleHt, getPicture = False):
    
    brainSplits = []

    for wid,height in attributes:
        wid = wid + 4
        height = height + 5
        singleBrainScan = picInGray[height:height + rectangleHt, wid + 4:wid + rectangleWt - 4]
        
        if cv2.countNonZero(singleBrainScan) > 10:
            if getPicture:
                cv2.rectangle(pic,(wid + 4,height),(wid + rectangleWt - 4, height + rectangleHt),(255,0,0),1)

            singleBrainScan = pic[height:height + rectangleHt, wid + 4:wid + rectangleWt - 4]
            brainSplits.append(singleBrainScan)

    return brainSplits

def makeSubFolder(brainDataLocation):
    makePath = os.path.exists(brainDataLocation)

    if not makePath:
        os.makedirs(brainDataLocation)

def createBoundariesMethod(brainParts, uniqueID, createdDirectory):
    makePath = os.path.exists(createdDirectory + "/" + uniqueID + "/")

    if not makePath:
        os.makedirs(createdDirectory + "/" + uniqueID + "/")

    for key, brainSplitted in enumerate(brainParts):
        cv2.imwrite(createdDirectory + "/" + uniqueID + "/" +  "_slice_" + uniqueID + str(key) + ".png", brainSplitted)

    createBound(uniqueID, createdDirectory + "/" + uniqueID + "/")


def createBound(uniqueID, oldDirectory):
    makeSubFolder(oldDirectory.replace("Slices", "Boundaries"))

    for key,brainSplit in enumerate(os.listdir(oldDirectory)):
        splittedPictre = cv2.imread(oldDirectory + "/" + brainSplit)

        result, thresh = cv2.threshold(cv2.cvtColor(splittedPictre, cv2.COLOR_BGR2GRAY), 50, 255, 0)
        contours, varContours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(splittedPictre, contours, -1, (51,255,255), 1)
        
        cv2.imwrite(oldDirectory.replace("Slices", "Boundaries") + "_boundary_" + uniqueID + str(key) + ".png", splittedPictre)    
        


def createSliceSubFolderMethod(pic, Directory, uniqueID, newDirectory):
    imageRead = cv2.imread(Directory + "/" + pic)
    h, w, d = imageRead.shape
    imageRead = imageRead[26:h, :w - 69]

    picInGray = cv2.cvtColor(imageRead, cv2.COLOR_BGR2GRAY)
    result, s = cv2.threshold(picInGray, 0, 255, cv2.THRESH_BINARY)
    getCont, varContours = cv2.findContours(s,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    attributesOnTop = []

    for x in getCont:
        i,j,w,h = cv2.boundingRect(x)

        if w == 4 and h <= 5:
            attributesOnTop.append((i,j))

    # removeDuplicates(attributesOnTop)
    attributesOnTop = [*set(attributesOnTop)]
    attributesOnTop.sort()
    brainParts = getSlices(imageRead, picInGray, attributesOnTop, 118, 118)

#    calling method to create boundaries folder
    createBoundariesMethod(brainParts, uniqueID, newDirectory)

# def removeDuplicates(val):
#     val = [*set(val)]

def parsePictures(brainScansPath):
    # create subfolders
    generateSubFolders()
    
    for subfolder in os.listdir(brainScansPath):
        if subfolder.split('.')[0].endswith("thresh"):
            createSliceSubFolderMethod(subfolder, brainScansPath, subfolder.split('.')[0][:subfolder.split('.')[0].rfind('_')], "Slices")

def generateSubFolders():
    makePath = os.path.exists("Slices")
    if not makePath:
        os.makedirs("Slices")

    makePath = os.path.exists("Boundaries")
    if not makePath:
        os.makedirs("Boundaries")


parsePictures(brainScansPath)