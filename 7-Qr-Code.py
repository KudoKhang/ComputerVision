import cv2
import numpy as np
from pyzbar.pyzbar import decode

im = cv2.imread('./images/CARD-1.png')

with open('dataQR.txt') as f:
    myDataList = f.read().splitlines()


for barcode in decode(im):
    # print(barcode)
    myData = barcode.data.decode('utf-8')
    print(myData)
    
    for data in myDataList:
        if myData in data:
            print(f"Welcome{data.split(',')[1]}")



    pts = np.array([barcode.polygon], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(im, [pts], True, (255,0,255), 5)
    pts2 = barcode.rect
    cv2.putText(im, myData, (pts2[0], pts2[1]), cv2.FONT_ITALIC, 0.9, (255, 0, 255), 2)

cv2.imshow('Result', im)
cv2.waitKey(0)
cv2.destroyAllWindows()