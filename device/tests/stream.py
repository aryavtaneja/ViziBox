import socket
import time

import numpy as np
import picamera

try:
    socket = socket.socket()
    socket.connect(('DESKTOP-RQTO4S9.local', 8000))
    connection = socket.makefile('wb')
    print(f"Connected to {socket.getpeername()}")
except Exception as e:
    print(f"Failed to connect: {e}")
    exit(1)

try:
    camera = picamera.PiCamera()
    camera.resolution = (480, 320)
    camera.framerate = 5
    camera.start_preview()  
    time.sleep(2)

    print(f'Beginning sending images to {socket.getpeername()}')

    while True:
        image = np.empty((320 * 480 * 3,), dtype=np.uint8)
        camera.capture(image, 'bgr')
        image = image.reshape((320, 480, 3))

        print(f'Sending image of size {image.size}')
        connection.write(image.tobytes())

        time.sleep(1)

finally:
    connection.close()
    socket.close()