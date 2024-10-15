from io import BytesIO
import socket
import time

import picamera
import picamera.array

camera = picamera.PiCamera()
camera.resolution = (1640, 1232)
camera.exposure_mode = 'sports'
time.sleep(2)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('', 8080)
sock.bind(server_address)

sock.listen(1)

while True:
    print('Waiting for a connection...')
    connection, client_address = sock.accept()
    print('Connection from', client_address)

    try:
        image = BytesIO()
        camera.capture(image, format='png')
        print('Captured image')

        image = image.getvalue()

        for x in range(0, len(image), 1024):
            connection.send(image[x:x+1024])

        print('Sent image to ', client_address)

    except Exception as e:
        print(e)

    finally:
        connection.close()