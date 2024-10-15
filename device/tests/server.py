import socket

import cv2
import numpy as np

socket = socket.socket()
socket.bind(('0.0.0.0', 8000))
print(f'Listening on {socket.getsockname()}')
socket.listen(0)    

connection = socket.accept()[0].makefile('rb')
print("Connected")

try:
    #the images are sent as openCV images
    #receive each image and imshow it
    while True:
        imagesize = 460800
        image = np.empty((imagesize,), dtype=np.uint8)
        connection.readinto(image)

        print(f'Received image of size {image.size}')
        image = image.reshape((320, 480, 3))
        cv2.imshow('image', image)
        cv2.waitKey(1)
        
finally:
    connection.close()
    socket.close()
