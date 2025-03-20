import asyncio
import websockets
import time

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

DANGER_CODES = {
    1: "FIRE",
    2: "CHOPPING TECHNIQUE",
    3: "LACERATION",
    4: "BURNS"
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

        # Send RESET message (to reset server state)
        input("Send Reset Signal...")
        await websocket.send(format_message(HEADERS["RST"]))
        response = await websocket.recv()
        print(f"Received: {response}")
        
        # Send SYN message (to initiate communication)
        await websocket.send(format_message(HEADERS["SYN"]))
        response = await websocket.recv()
        print(f"Received: {response}")
        
        # # Send DATA messages in sequence
        # for i in range(3):
        await websocket.send(format_chopped_message(HEADERS["DATA"], 0, f"roughly chop onion"))
        response = await websocket.recv()
        print(f"Received: {response}")

        await websocket.send(format_chopped_message(HEADERS["DATA"], 1, f"slice onion"))
        response = await websocket.recv()
        print(f"Received: {response}")

        await websocket.send(format_chopped_message(HEADERS["DATA"], 2, f"caramelize onion"))
        response = await websocket.recv()
        print(f"Received: {response}")

        await websocket.send(format_chopped_message(HEADERS["DATA"], 3, f"All Done!"))
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
        
        # Send NEXT message (to move to the next step) USER INITIATED
        input("Press Enter to send NEXT...")
        await websocket.send(format_message(HEADERS["NEXT"], "1"))
        print("Sent Next")
        response = await websocket.recv()
        print(f"Received: {response}") # expected response ACK:NEXT

        # Test Interrupt
        response = await websocket.recv() 
        print(f"Received: {response}") # expected response Interrupt:Chopping Technique 60:2
        await websocket.send(format_message(HEADERS["ACK"], HEADERS["INTR"])) # ACK Interrupt
        input("Press Enter to send PASS...")
        await websocket.send(format_message(HEADERS["PASS"], "2")) # send pass
        print(f"PASS Sent")
        response =  await websocket.recv()
        print(f"Received: {response}") # expected response ACK:PASS

        await websocket.send(format_message(HEADERS["PRV"], "1"))
        response = await websocket.recv()
        print(f"Received: {response}") # expected response ACK:PRV
        await websocket.send(format_message(HEADERS["NEXT"], "2"))
        response = await websocket.recv()
        print(f"Received: {response}") # expected response ACK:NEXT

        # ML Initiated NEXT
        input("Press Enter when showing carmelized onion...")
        response = await websocket.recv() # show carmelized onion
        print(f"Received: {response}") # expected msg NEXT:
        await websocket.send(format_message(HEADERS["ACK"], HEADERS["NEXT"]))
        
        # Send RESET message (to reset server state)
        input("Send Reset Signal...")
        await websocket.send(format_message(HEADERS["RST"]))
        response = await websocket.recv()
        print(f"Received: {response}")

        print("Test completed.")

# Run the test
asyncio.run(test_websocket())
