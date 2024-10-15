import socket

HOST = '192.168.4.1'  # Replace with the IP address of your Pi Zero
PORT = 8080       # Replace with the port number used in your Pi Zero script

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the Pi Zero
    s.connect((HOST, PORT))
    print("Connected to Raspberry Pi Zero")

    while True:
        # Send a test message to the Pi Zero
        message = "Hello from Windows!"
        s.sendall(message.encode())

        # Receive data from the Pi Zero
        data = s.recv(1024)
        if not data:
            break
        print("Received data:", data.decode())

except Exception as e:
    print("Error:", e)

finally:
    # Close the socket
    s.close()