import cv2
import numpy as np

img = cv2.imread('./images/oto.jpg')
kernel = np.ones((3,3),np.uint8)

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlue = cv2.GaussianBlur(imgGray, (7,7), 0)
imgCanny = cv2.Canny(img,100, 200)
imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)  # dilate = gian ra
imgEroded = cv2.erode(imgDialation, kernel, iterations=2)  # erode = xoi mon
cv2.imshow('Canny', imgCanny)
cv2.imshow('Dialation', imgDialation)
cv2.imshow('Eroded', imgEroded)
cv2.waitKey(0)

# iterations la so lan ap dung kernel



# img = cv2.imread("resources/2.jpg")
# img = cv2.resize(img, (480, 640))
# kernal = np.ones((5,5), np.uint8)
#
# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# imgBlue = cv2.GaussianBlur(imgGray, (7,7), 0)
# imgCanny = cv2.Canny(img, 100, 100) # lay ra anh Trang - Den
# imgDialation = cv2.dilate(imgCanny, kernal, iterations=1) # Khuech dai diem sang
# imgEroded = cv2.erode(imgDialation, kernal, iterations=10) # Khuech dai diem toi
#
# # cv2.imshow("Grray", imgGray)
# # cv2.imshow("Blue", imgGray)
# # cv2.imshow("Canny", imgCanny)
# cv2.imshow("Dialation", imgDialation)
# cv2.imshow("Eroded", imgEroded)
# cv2.waitKey(0)