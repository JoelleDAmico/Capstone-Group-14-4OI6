import asyncio
import websockets

# Server address
SERVER_URI = "ws://localhost:8765"

# Headers to match the ones in your server
HEADERS = {
    "ACK": "1",
    "SYN": "10",
    "DATA": "11",
    "NEXT": "12",
    "PRV": "13",
    "FIN": "20",
    "RST": "30",
    "HEARTBEAT": "40",
    "INTR": "60",
    "PASS": "70",
    "INVALID": "FF"
}

# Function to format a message
def format_message(header, payload=""):
    return f"{header}:{payload}"

# function to format multi-part messages 
def format_chopped_message(header, sequence, payload=""):
    return f"{header}:{sequence}:{payload}"

# Function to send test messages
async def test_websocket():
    async with websockets.connect(SERVER_URI) as websocket:
        
        print("Connected to WebSocket server.")
        
        # Send SYN message (to initiate communication)
        await websocket.send(format_message(HEADERS["SYN"]))
        response = await websocket.recv()
        print(f"Received: {response}")
        
        # # Send DATA messages in sequence
        # for i in range(3):
        await websocket.send(format_chopped_message(HEADERS["DATA"], 1, f"slice onion"))
        response = await websocket.recv()
        print(f"Received: {response}")

        await websocket.send(format_chopped_message(HEADERS["DATA"], 2, f"roughly chop onion"))
        response = await websocket.recv()
        print(f"Received: {response}")

        await websocket.send(format_chopped_message(HEADERS["DATA"], 3, f"caramelize onion"))
        response = await websocket.recv()
        print(f"Received: {response}")
        
        # Send FIN message (to indicate end of data transfer)
        await websocket.send(format_message(HEADERS["FIN"]))
        response = await websocket.recv()
        print(f"Received: {response}")
        
        # Send HEARTBEAT message (to check connection health)
        await websocket.send(format_message(HEADERS["HEARTBEAT"]))
        response = await websocket.recv()
        print(f"Received: {response}")
        
        # Send NEXT message (to move to the next step)
        await websocket.send(format_message(HEADERS["NEXT"], "1"))
        response = await websocket.recv()
        print(f"Received: {response}")
        
        # Send RESET message (to reset server state)
        # await websocket.send(format_message(HEADERS["RST"]))
        # response = await websocket.recv()
        # print(f"Received: {response}")

        print("Test completed.")

# Run the test
asyncio.run(test_websocket())
