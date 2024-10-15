from time import sleep
import cv2
import pytesseract
import numpy as np

img = cv2.imread('image.jpg')

img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

kernel = np.ones((1, 1), np.uint8)
img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)

cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

cv2.imshow('image', img)
cv2.waitKey(0)

text = pytesseract.image_to_string(img, config='--oem 3 --psm 6')
print(text)