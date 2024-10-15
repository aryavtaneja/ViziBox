import socket
import time

import picamera
import picamera.array
import pytesseract

# Start the camera and wait for it to warm up
camera = picamera.PiCamera()
camera.resolution = (640, 480)  # Update resolution here
camera.framerate = 5
camera.start_preview()
time.sleep(2)

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP address and port
server_address = ('', 8080)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Accept incoming connections and serve the text data
while True:
    # Wait for a client to connect
    print('Waiting for a connection...')
    connection, client_address = sock.accept()
    print('Connection from', client_address)

    try:
        while True:
            # Capture an image from the camera
            image = picamera.array.PiRGBArray(camera)
            camera.capture(image, format='rgb')
            image = image.array

            # Convert the image to grayscale
            image = image.mean(axis=2).astype('uint8')

            # Apply the pytesseract image to string function
            text = pytesseract.image_to_string(image)

            if text.strip() == "":
                text = "No text"

            print(text)

            # Send the text data to the client
            connection.sendall(text.encode())

    except Exception as e:
        print(e)

    finally:
        # Clean up the connection
        connection.close()