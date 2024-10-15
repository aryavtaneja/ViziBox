import asyncio
import io
import struct

import picamera
import websockets
from gpiozero import Button

button = Button(2)

async def start_server(websocket, path):
    camera = picamera.PiCamera()
    camera.resolution = (1640, 1232)
    camera.framerate = 5
    camera.exposure_mode = 'sports'
    await asyncio.sleep(2)  # Wait for the camera to stabilize

    print("Camera started. Beginning capture...")

    try:
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            try:
                # Write the length of the capture to the stream and flush
                # to ensure it actually gets sent before the image data
                connection_data = struct.pack('<L', stream.tell())
                if button.is_pressed:
                    await websocket.send(connection_data)
                    await websocket.send(stream.getvalue())
                    print("Frame sent.")
                else:
                    await websocket.send('ping')
            except websockets.exceptions.ConnectionClosedError:
                print("Connection broken. Exiting frame capture...")
                break  # Exit the loop when the connection is broken

            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()

    finally:
        camera.close()  # Ensure camera is closed before restarting the server
        print("Capture complete.")
        print("Restarting server...")

async def main():
    while True:  # Add a loop to restart the server if a connection is lost
        try:
            server = await websockets.serve(start_server, '0.0.0.0', 8000)
            print("WebSocket server initialized. Waiting for client connection...")
            await server.wait_closed()
        except websockets.exceptions.ConnectionClosedError:
            print("Connection lost. Restarting server...")
        except Exception as e:
            print(f"Unexpected error: {e}. Restarting server...")

# Run the WebSocket server
asyncio.run(main())