import socket
import numpy as np
import cv2

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's IP address and port
server_address = ('riadevice.local', 8080)
sock.connect(server_address)

try:
    # Initialize the image buffer
    image_buffer = b''

    while True:
        # Receive the image data from the server in chunks
        data = sock.recv(1024)

        if not data:
            break

        # Append the received data to the image buffer
        image_buffer += data

    with open('received_image.png', 'wb') as img_file:
        #display image with opencv
        img_file.write(image_buffer)
        img = cv2.imread("received_image.png")
        cv2.imshow('Received Image', img)
        cv2.waitKey(0)

finally:
    # Clean up the connection
    sock.close()