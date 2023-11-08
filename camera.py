import asyncio
import websockets
import cv2
import numpy as np
import base64
import json
import base64
from PIL import Image
from io import BytesIO

async def handle_connection(websocket, path):
    print('Handle Connection')
        
    while True:
        try:
            print('Start connection')
            message = await websocket.recv()
            data = json.loads(message)
            frame_data = data.get('data', '')  # Lấy dữ liệu hình ảnh từ 'data'
            if frame_data != 'data:,':
                print(frame_data)
                # Decode the base64 data
                image_data = base64.b64decode(frame_data)

                # Create a BytesIO object to open the image with PIL
                image_bytes = BytesIO(image_data)

                # Open and display the image
                image = Image.open(image_bytes)
                image.show()
                # Lỗi ở đây
                # image_bytes = base64.b64decode(frame_data)
                # image_data = cv2.imdecode(np.frombuffer(
                #     image_bytes, np.uint8), cv2.IMREAD_COLOR)

                # # Process the image if needed
                # gray_frame = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
                # _, buffer = cv2.imencode('.jpg', gray_frame)
                # image_data_bytes = buffer.tobytes()
                # base64_data = base64.b64encode(image_data_bytes).decode('utf-8')
            else:
                base64_data = ''
            # Convert the processed image to a base64-encoded data URI
            f64_decode = base64_data
            # f64_decode = f'data:image/jpeg;base64,{base64_data}'

            # Send a response with the processed image data
            json_data = {
                'image': f64_decode,
                'emotions': 'results'
            }
            json_string = json.dumps(json_data)
            await websocket.send(json_string)
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            break

global host_setup, port_setup
host_setup = "192.168.88.30"
port_setup = 4111

if __name__ == '__main__':
    print('check_is_socket is True')
    start_server = websockets.serve(handle_connection, host_setup, port_setup)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
