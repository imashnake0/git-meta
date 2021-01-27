from cv2 import cv2 
import numpy as np

import processImg as pimg

################################################################
# input values
path = "resources/LFIA_list.jpg"
# top right and bottom left of a reactangle's coordinates
coordinates = [[259, 163],[374, 193]]

################################################################
# Image Analysis
def countContours(img):
    count = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 150:
            cv2.drawContours(imgContour, cnt, -1, (255, 255, 255), 3)
            count += 1
            x, y, w, h = cv2.boundingRect(cv2.approxPolyDP(cnt, 0.05*cv2.arcLength(cnt, True), True))
            cv2.rectangle(imgContour,(x, y), (x+w, y+h), (0,255,0), 3)

    return count
###############################################################################################################
# main

print("check1")
img = cv2.imread(path)
print("check2")

img = pimg.resizeImage(img)
cv2.imshow("resized", img)

img = pimg.cropImg(img, coordinates[0][1], coordinates[0][0], coordinates[1][1], coordinates[1][0])
cv2.imshow("crop", img) # TESTTTTTTTTTTTTTTTTTTTTTTTTTTTT

imgPorcessed = pimg.imgPorcessingSimple(img)
cv2.imshow("processed", imgPorcessed)
imgContour = img.copy()
contourNum = countContours(imgPorcessed)

cv2.imshow("contours", imgContour) # TESTTTTTTTTTTTTTTTTTTTTTTTTTTTT
 
print("number of lines ", contourNum-1)
cv2.waitKey(0)

