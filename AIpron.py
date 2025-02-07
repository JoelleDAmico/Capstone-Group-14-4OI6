import asyncio
import websockets
import threading
import time

# Variables
current_state = "IDLE"  # States: IDLE, RECEIVING, SENDING, INTERRUPT, PAUSED
previous_state = "" # used when returning to pre-interrupt state (and possibly to track debug flow)
received_payload = []
special_steps = []
instruction_payload = ""
interrupt_code = 0
interrupt_active = False
data_to_send = False
next_counter = 0
step_index = 0
recipe_ready = False

KEYWORDS = []

lock = threading.Lock()
send_event = asyncio.Event()

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

# function to format messages
def format_message(header, payload=""):
    return f"{header}:{payload}"

# function to format multi-part messages 
def format_chopped_message(header, sequence, payload=""):
    return f"{header}:{sequence}:{payload}"

# function to parse messages
def parse_message(message):
    parts = message.split(":")
    header = parts[0]
    if len(parts) > 2:
        sequence = parts[1]
        payload = parts[2]
    elif len(parts) > 1:
        payload = parts[1]
        sequence = ""
    return header, payload, sequence

# function to handle received messages (incoming)
async def process_incoming(websocket):

    global current_state, received_payload, instruction_payload, previous_state, interrupt_code, next_counter, step_index, recipe_ready
    
    async for message in websocket:
            print(message)
                
            header, payload, sequence = parse_message(message)

            if current_state == "IDLE" and header == HEADERS["SYN"]:
                print("Client initiating data transfer.")
                previous_state = current_state
                current_state = "RECEIVING"
                await websocket.send(format_message(HEADERS["ACK"], "SYN"))

            elif current_state == "RECEIVING":
                if header == HEADERS["FIN"]:
                    print("Client indicated end of payload.")
                    recipe_ready = True
                    extract_watch_steps()
                    previous_state = current_state
                    current_state = "IDLE"
                    await websocket.send(format_message(HEADERS["ACK"], "FIN"))
                else:
                    received_payload.append(payload)
                    print(f"Received chunk {sequence}: {payload}")
                    await websocket.send(format_message(HEADERS["ACK"], sequence))

            elif current_state == "PAUSED":
                if header == HEADERS["PASS"] and payload == interrupt_code:
                    print("Pass message received from client. Resuming operation.")
                    current_state = previous_state
                    await websocket.send(format_message(HEADERS["ACK"], "PASS"))

            elif header == HEADERS["RST"]:
                print("Resetting to idle state.")
                previous_state = current_state
                current_state = "IDLE"  # States: IDLE, RECEIVING, SENDING, INTERRUPT, PAUSED
                received_payload = []
                instruction_payload = ""
                interrupt_code = 0
                next_counter = 0
                step_index = 0
                recipe_ready = False
                await websocket.send(format_message(HEADERS["ACK"], "RESET"))

            elif header == HEADERS["HEARTBEAT"]:
                print("Heartbeat received.")
                await websocket.send(format_message(HEADERS["ACK"], "HEARTBEAT"))

            elif header == HEADERS["NEXT"]:
                if(payload == "NO"):
                    next_counter += 1
                    previous_state = current_state
                    current_state = "IDLE"
                else:
                    next_counter += 1
                    decider, current_result = run_diagnostic()

                    if(decider == False and next_counter < 2):
                        await websocket.send(format_message(HEADERS["NEXT"], current_result))
                    else:
                        next_counter = 0
                        await websocket.send(format_message(HEADERS["ACK"], HEADERS["NEXT"]))
                        step_index = payload
                        previous_state = current_state
                        current_state = "IDLE"

            elif header == HEADERS["ACK"] and payload == HEADERS["NEXT"]:
                step_index+=1
                previous_state = current_state
                current_state = "IDLE"

            elif header == HEADERS["PRV"]:
                step_index = payload
                await websocket.send(format_message(HEADERS["ACK"], HEADERS["PRV"]))

            else:
                print(f"Unexpected message: {message}")
                await websocket.send(format_message(HEADERS["INVALID"], message))
                previous_state = current_state
                current_state = "IDLE"

# asyncio coroutine necessity
async def set_send():
    send_event.set()

# process sending data
async def process_sending(websocket):
    global current_state, received_payload, instruction_payload, previous_state, interrupt_code, interrupt_active, data_to_send

    while 1:
        await send_event.wait()
        send_event.clear()
        with lock:
                try:
                    if current_state == "INTERRUPT":
                        interrupt_message = format_message(HEADERS["INTR"], interrupt_code)
                        while 1:
                            await websocket.send(interrupt_message)
                            print(f"Sent interrupt: {DANGER_CODES[interrupt_code]}")
                            try:
                                ack = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                                header, payload, _ = parse_message(ack)
                                if header == HEADERS["ACK"] and payload == HEADERS["INTR"]:
                                    print(f"ACK received! Waiting for pass...")
                                    current_state = "PAUSED"
                                    break

                            except asyncio.TimeoutError:
                                print(f"ACK timeout. Resending Interrupt Signal...")

                    elif current_state == "SENDING":
                        syn_message = format_message(HEADERS["SYN"])
                        await websocket.send(syn_message)
                        print(f"Trying to start data transfer...")
                        ack_received = await websocket.recv()
                        header, payload, _ = parse_message(ack_received)

                        if header == HEADERS["ACK"] and payload == HEADERS["SYN"]:
                            print(f"ACK received! Starting data transfer...")
                            await send_data(websocket)

                except Exception as e:
                    print(f"Error sending: {e}")
           
# WebSocket handler
async def websocket_handler(websocket):
    global current_state, received_payload, instruction_payload, previous_state

    receive_task = asyncio.create_task(process_incoming(websocket))
    send_task = asyncio.create_task(process_sending(websocket))

    try:
        await asyncio.gather(receive_task, send_task)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        receive_task.cancel()
        send_task.cancel()

# Function to send data
async def send_data(websocket):
    global instruction_payload, current_state

    data = instruction_payload
    chunk_size = 28
    sequence = 0
    last_acked_seq = -1

    while data:
        chunk, data = data[:chunk_size], data[chunk_size:]
        message = format_chopped_message(HEADERS["DATA"], sequence, chunk)

        while last_acked_seq != sequence:
            await websocket.send(message)
            print(f"Sent chunk {sequence}: {chunk}")

            try:
                ack = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                header, seq_num, _ = parse_message(ack)
                if header == HEADERS["ACK"] and seq_num == sequence:
                    print(f"Receieved ack for chunk {sequence}.")
                    last_acked_seq = sequence
                    break

            except asyncio.TimeoutError:
                print(f"ACK timeout. Resending...")

        sequence += 1
        await asyncio.sleep(0.5)

    # Send FIN message
    fin_message = format_message(HEADERS["FIN"])
    await websocket.send(fin_message)
    print("All data sent. Sent FIN message.")
    current_state = "IDLE"

# separate thread function to discern send conditions
def send_cases(loop):
    global current_state, received_payload, instruction_payload, previous_state, interrupt_code, interrupt_active, data_to_send

    while True:
        with lock:
            if (interrupt_active):
                interrupt_code = 1
                previous_state = current_state
                current_state = "INTERRUPT"
                interrupt_active = False
                asyncio.run_coroutine_threadsafe(set_send(), loop)


            elif (data_to_send):
                instruction_payload = "Quando autem elevatum est cor eius, et spiritus illius obfirmatus est ad superbiam, depositus est de solio regni sui, et gloria eius ablata est et a filiis hominum eiectus est, sed et cor eius cum bestiis positum est, et cum onagris erat habitatio eius: foenum quoque ut bos comedebat, et rore caeli corpus eius infectum est, donec cognosceret quod potestatem haberet Altissimus in regno hominum: et quemcumque voluerit, suscitabit super illud."  # Data to be sent to central
                current_state = "SENDING"
                data_to_send = False
                asyncio.run_coroutine_threadsafe(set_send(), loop)
            
            else:
                pass

            time.sleep(0.5)

# Start WebSocket server
async def start_server():
    async with websockets.serve(websocket_handler, "localhost", 8765):
        print("Server Running!")

        # Start send_cases in a separate thread
        loop = asyncio.get_event_loop()
        cases_thread = threading.Thread(target=send_cases, args=(loop,), daemon=True)
        # ML_thread = threading.Thread(target=ML_func, args=(loop,), daemon=True)
        cases_thread.start()
        # ML_thread.start()

        await asyncio.Future()  # run forever

# Extract Special Steps
def extract_watch_steps():
    global recipe_ready, received_payload, step_index, special_steps

    if (recipe_ready):
        for i in received_payload:
            for x in KEYWORDS:
                if x in i:
                    special_steps.append(i)


# Machine Learning Detection
# def ML_func():

#     global step_index, special_steps

#     while True:
#         with lock:
#             if step_index in special_steps:
#                 """ activate relevant ML algorithm """
            

# main
if __name__ == "__main__":

    # Run WebSocket server
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("\nStopping WebSocket server.")