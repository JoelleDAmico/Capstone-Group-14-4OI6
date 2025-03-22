import threading
import time
import websocket #As opposed to websockets, which was used in the rpi side

# Server address
SERVER_URI = "ws://localhost:8765"

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

interrupt_code = 0
step_index = 0

# Function to format a message
def format_message(header, payload=""):
    return f"{header}:{payload}"

# Function to format multi-part messages
def format_chopped_message(header, sequence, payload=""):
    return f"{header}:{sequence}:{payload}"

# Function to parse messages
def parse_message(message):
    parts = message.split(":")
    header = parts[0]
    sequence = parts[1] if len(parts) > 2 else ""
    payload = parts[2] if len(parts) > 2 else (parts[1] if len(parts) > 1 else "")
    return header, sequence, payload

# Function to handle receiving messages
def receive_messages(ws):
    global interrupt_code, step_index
    print("[RECEIVE] Listening for messages...")

    while True:
        try:
            message = ws.recv()
            print(f"[RECEIVE] Received raw message: {message}")

            header, sequence, payload = parse_message(message)

            if header == HEADERS["INTR"]:
                print(f"Interrupt Received: {DANGER_CODES.get(int(payload), 'UNKNOWN')}! Take action.")
                interrupt_code = int(payload)
                msg = format_message(HEADERS["ACK"], HEADERS["INTR"])
                ws.send(msg)
            elif header == HEADERS["NEXT"]:
                print(f"Machine initiated next to step: {payload}. Reported Result: {sequence}.")
                step_index = int(payload)
                msg = format_message(HEADERS["ACK"], HEADERS["NEXT"])
                ws.send(msg)
            else:
                print(f"Received: {message}")

        except websocket.WebSocketConnectionClosedException:
            print("[RECEIVE] Connection closed by server.")
            break
        except Exception as e:
            print(f"[RECEIVE] Unexpected error: {e}")
            break

# Function to handle sending messages
def send_messages(ws):
    global interrupt_code, step_index

    while True:
        ui = input("Enter command (IS - Instruction Set, N - Next, PR - Previous, IP - Pass, R - Reset): ")

        if ui == "IS":
            ws.send(format_message(HEADERS["SYN"]))
            ws.send(format_chopped_message(HEADERS["DATA"], 0, "roughly chop onion"))
            ws.send(format_chopped_message(HEADERS["DATA"], 1, "slice onion"))
            ws.send(format_chopped_message(HEADERS["DATA"], 2, "caramelize onion"))
            ws.send(format_chopped_message(HEADERS["DATA"], 3, "All Done!"))
            ws.send(format_message(HEADERS["FIN"]))

        elif ui == "N":
            step_index += 1
            msg = format_message(HEADERS["NEXT"], str(step_index))
            ws.send(msg)
            print(f"Sent N: {msg}")

        elif ui == "PR":
            step_index = max(0, step_index - 1)
            msg = format_message(HEADERS["PRV"], str(step_index))
            ws.send(msg)
            print(f"Sent PR: {msg}")

        elif ui == "IP":
            msg = format_message(HEADERS["PASS"], str(interrupt_code))
            ws.send(msg)
            print(f"Sent PASS: {msg}")

        elif ui == "R":
            step_index = 0
            interrupt_code = 0
            msg = format_message(HEADERS["RST"])
            ws.send(msg)
            print(f"Sent RST: {msg}")

# Main function to start the WebSocket client
def websocket_client():
    ws = websocket.WebSocket()
    ws.connect(SERVER_URI)

    print("[CLIENT] Connected to WebSocket server.")

    receive_thread = threading.Thread(target=receive_messages, args=(ws,))
    receive_thread.daemon = True
    receive_thread.start()

    send_messages(ws)

websocket_client()