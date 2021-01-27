import copy
from cv2 import cv2 
import numpy as np
# from skimage import measure

widthImg = 640 # TESTTTTTTTTTTTTTTTTTTTTTTTTTTTT
heightImg = 480 # TESTTTTTTTTTTTTTTTTTTTTTTTTTTTT
################################################    
# imgPorcessing function - by Ben Z.
# 1. read raw image, already grayscale
# 2. equalize the image in the first step to getting a binary (black/white) image
# 3. do an adaptive threshold to get a black/white image, still got lots of noise
# 4. perform an erosion to remove any very small dots of noise from the thresholded image
# 5. perform a connected component analysis on the thresholded image, then store only the "large" blobs into mask
# 6. skeletonize mask into skel
# 7. dilate image for increased accuracy on vertical line identification
def imgPorcessing(src):
    # imgContrast = contrastImage(src)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    dst = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,41,10)  
    erode1 = cv2.erode(dst, None, iterations=1)

    labels = measure.label(erode1, connectivity=2, background=0)
    mask = np.zeros(erode1.shape, dtype="uint8")
    for label in np.unique(labels):
        # if this is the background label, ignore it
        if label == 0:
            continue
        # otherwise, construct the mask for this label and count the number of pixels
        labelMask = np.zeros(erode1.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)

        # if the number of pixels in the component is sufficiently
        # large, then add it to our mask of "large blobs"
        if numPixels > 200:
            # add the blob into mask
            mask = cv2.add(mask, labelMask)

    # Skeleton    
    img = copy.copy(mask)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    done = False
    size = np.size(img)
    # the skeleton is initially all black
    skel = np.zeros(img.shape,np.uint8)     
    while( not done):
        eroded = cv2.erode(img,element)
        temp = cv2.dilate(eroded,element)
        temp = cv2.subtract(img,temp)
        skel = cv2.bitwise_or(skel,temp)
        img = eroded.copy()
        zeros = size - cv2.countNonZero(img)
        if zeros==size:
            done = True

    return cv2.dilate(skel, None, iterations=1)

################################################################################################################
def cropImg(img,x,y,w,h):
    return img[x:w, y:h]


def resizeImage(img):
    imgResized = cv2.resize(img, (widthImg, heightImg))  # TESTTTTTTTTTTTTTTTTTTTTTTTTTTTT
    return cropImg(imgResized, 40 , 40 , imgResized.shape[0]-40, imgResized.shape[1]-40)


def contrastImage(imgResized):
    lab = cv2.cvtColor(imgResized, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    # cv2.imshow('l_channel', l)
    # cv2.imshow('a_channel', a)
    # cv2.imshow('b_channel', b)

    # -----Applying CLAHE to L-channel-----
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    # cv2.imshow('CLAHE output', cl)

    # -----Converting image from LAB Color model to RGB model-----
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


def imgPorcessingSimple(img):
    imgContrast = contrastImage(img)

    gray = cv2.cvtColor(imgContrast, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    kernal = np.ones((5, 5), np.uint8)
    imgDial = cv2.dilate(blur, kernal, iterations=2)
    imgErod = cv2.erode(imgDial, kernal, iterations=1)

    ret3, th3 = cv2.threshold(imgErod, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3



