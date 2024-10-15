import socket
from pynput.keyboard import Key, Listener

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's IP address and port
server_address = ('192.168.4.1', 8080)
sock.connect(server_address)

try:
    while True:
        # Receive the text data from the server
        data = sock.recv(1024)

        if not data:
            break

        # Decode the received data and print it
        text = data.decode()

        #if the p key is pressed on the keyboard, print the text
        def on_press(key):
            if key == Key.up:
                print(text)

        with Listener(on_press=on_press) as listener:
            listener.join()

finally:
    # Clean up the connection
    sock.close()