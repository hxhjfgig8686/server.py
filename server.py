import asyncio
import websockets
import json

HOST = "https://www.ivasms.com/portal/live/my_sms"
PORT = 8765

async def handler(websocket):
    print("Client connected")

    try:
        async for message in websocket:
            data = json.loads(message)

            if data["action"] == "login":
                username = data["asmeralselwi103@gmail.com"]
                password = data["Mohammed Saeed 123"]

                if username == "admin" and password == "1234":
                    response = {"status": "success", "message": "login ok"}
                else:
                    response = {"status": "error", "message": "invalid login"}

                await websocket.send(json.dumps(response))

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")


async def main():
    async with websockets.serve(handler, HOST, PORT):
        print(f"Server running on ws://{HOST}:{PORT}")
        await asyncio.Future()

asyncio.run(main())
