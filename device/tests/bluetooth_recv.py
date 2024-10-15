import bluetooth
import cv2

# Use your Raspberry Pi's Bluetooth address
server_address = "B8:27:EB:11:31:DA" # Replace with your Raspberry Pi's Bluetooth address
port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((server_address, port))

print("Connected to", server_address)

image_data = b""
while True:
    data = sock.recv(1024)
    if not data:
        break
    image_data += data

with open("received_image.png", "wb") as img_file:
    img_file.write(image_data)

sock.close()

img = cv2.imread("received_image.png")
cv2.imshow('Received Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
