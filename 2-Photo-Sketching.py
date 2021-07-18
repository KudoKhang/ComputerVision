import cv2
import numpy as np

def pencilSketch(img_rgb):
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    img_gray_inv = 255 - img_gray
    img_blur = cv2.GaussianBlur(img_gray_inv, (21,21), 0, 0)
    imgblend = cv2.divide(img_gray, 255 - img_blur, scale=256)
    # cv2.imshow('gray_inv', img_gray_inv)
    # cv2.imshow('blur', img_blur)
    # cv2.imshow('gray', img_gray)
    return cv2.cvtColor(imgblend, cv2.COLOR_GRAY2RGB)

img_rgb = cv2.imread('./images/photo-sketching.jpg')
result = pencilSketch(img_rgb)
horizontal = np.concatenate((img_rgb, result), axis=1)
cv2.imshow('result', horizontal)
cv2.waitKey(0)
