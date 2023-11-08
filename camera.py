import asyncio
import websockets
import cv2
import numpy as np
import base64
import json

async def on_message(websocket, path):
    async for message in websocket:
        data = json.loads(message)

        if data["message"] == "sendMessage":
            frame_data = data["data"]
            await process_and_send_emotion(frame_data, websocket)

async def process_and_send_emotion(frame_data, websocket):
    if frame_data != 'data:,':
        
        frame_data = frame_data.split(',')[1]
        # Decode the base64 frame data
        decoded_data = base64.b64decode(frame_data)
        # Convert frame data to a NumPy array
        np_data = np.fromstring(decoded_data,np.uint8)
        # Decode the image using OpenCV
        image_data = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)

        # Encode the processed image back to base64
        if not image_data.size:
            print("Error: Invalid image data")
        else:
            # Continue with the image encoding
            _, buffer = cv2.imencode('.jpg', image_data)
            image_data_bytes = buffer.tobytes()
            base64_data = base64.b64encode(image_data_bytes).decode('utf-8')
            f64_decode = f'data:image/png;base64,{base64_data}'
    else:
        f64_decode = f'data:image/png;base64,'

    # Send the processed image back to the client
    await websocket.send(json.dumps({
        "message": "processedImage",
        "image": f64_decode,
    }))

if __name__ == '__main__':
    host_setup = "192.168.88.30"
    port_setup = 4111
    print('check_is_socket is True')
    start_server = websockets.serve(on_message, host_setup, port_setup)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
