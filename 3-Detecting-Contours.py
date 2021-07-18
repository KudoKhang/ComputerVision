import cv2
import numpy as np

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area > 500:
            cv2.drawContours(imgContours, cnt, -1, (25,45,255), 2)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            # print(len(approx))
            object = len(approx)
            x,y,w,h = cv2.boundingRect(approx)
            
            if object == 3 : objType = "Tri"
            elif object == 6 : objType = "Hex"
            elif object == 8 : objType = "Cir"
            elif object == 4:
                ratio = w/float(h)
                if ratio > 0.95 and ratio < 1.05 : objType = "Square"
                else: object = "Rectangle"
            else: objType = "None"
                
            cv2.rectangle(imgContours, (x,y), (x+w, y+h), (255,0,255), 2)
            cv2.putText(imgContours, objType, (x + (w//2) - 15, y + (h//2)), cv2.FONT_ITALIC, 0.5, (255,255,0), 2)

path = './images/detecting-contours.jpg'
img = cv2.imread(path)
imgContours = img.copy()

imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)
imgCanny = cv2.Canny(imgBlur, 100, 100)

getContours(imgCanny)
cv2.imshow('canny', imgCanny)
cv2.imshow('imgcontours', imgContours)
cv2.waitKey(0)