import asyncio
import websockets
import threading
import time
import torch
import cv2
import warnings
import copy
import pathlib

pathlib.WindowsPath = pathlib.PosixPath

warnings.filterwarnings("ignore", category=UserWarning)

# Variables
current_state = "IDLE"  # States: IDLE, RECEIVING, SENDING, INTERRUPT, PAUSED, NEXT, RESET
previous_state = "" # used when returning to pre-interrupt state (and possibly to track debug flow)
received_payload = []
instruction_payload = ""
interrupt_code = 0
interrupt_active = False
ldata_to_send = False
send_next = False
step_index = 0
recipe_ready = False
current_result = ""
desired_result = ""


KEYWORDS = ["BLONDE COOK", "GOLDEN COOK", "CARAMELIZE COOK", "FINELY DICE", "ROUGH CHOP", "SLICE"]

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

    global current_state, received_payload, instruction_payload, previous_state, interrupt_code, step_index, recipe_ready, current_result, send_next, interrupt_active, ldata_to_send, desired_result
    
    async for message in websocket:
            print(message)
            print(current_state)
                
            header, payload, sequence = parse_message(message)

            if current_state == "IDLE" and header == HEADERS["SYN"]:
                print("Client initiating data transfer.")
                previous_state = current_state
                current_state = "RECEIVING"
                await websocket.send(format_message(HEADERS["ACK"], HEADERS["SYN"]))

            elif current_state == "RECEIVING":
                if header == HEADERS["FIN"]:
                    print("Client indicated end of payload.")
                    recipe_ready = True
                    previous_state = current_state
                    print(received_payload)
                    current_state = "IDLE"
                    await websocket.send(format_message(HEADERS["ACK"], HEADERS["FIN"]))
                else:
                    received_payload.append(payload)
                    print(f"Received chunk {sequence}: {payload}")
                    await websocket.send(format_message(HEADERS["ACK"], sequence))

            elif current_state == "PAUSED":
                if header == HEADERS["PASS"]:
                    print("Pass message received from client. Resuming operation.")
                    current_state = previous_state
                    await websocket.send(format_message(HEADERS["ACK"], HEADERS["PASS"]))

            elif header == HEADERS["RST"]:
                print("Resetting to idle state.")
                previous_state = current_state
                recipe_ready = False
                step_index = 0
                received_payload = []
                send_next = False
                interrupt_active = False
                ldata_to_send = False
                interrupt_code = 0
                current_result = ""
                desired_result = ""
                current_state = "IDLE"
                instruction_payload = ""
                await websocket.send(format_message(HEADERS["ACK"], HEADERS["RESET"]))

            elif header == HEADERS["HEARTBEAT"]:
                print("Heartbeat received.")
                await websocket.send(format_chopped_message(HEADERS["ACK"], current_state, HEADERS["HEARTBEAT"]))

            elif header == HEADERS["NEXT"]:
                await websocket.send(format_message(HEADERS["ACK"], HEADERS["NEXT"]))
                step_index = int(payload)
                print(f"User-Initiated Next, moving to step: {step_index}")
                previous_state = current_state
                current_state = "IDLE"

            elif current_state == "NEXT":
                if (header == HEADERS["ACK"]) and (payload == HEADERS["NEXT"]):
                    step_index+=1
                    print(f"ML-Initiated Next, moving to step: {str(step_index)}")
                    previous_state = current_state
                    current_state = "IDLE"

            elif header == HEADERS["PRV"]:
                step_index = int(payload)
                print(f"Returned to step: {step_index}")
                await websocket.send(format_message(HEADERS["ACK"], HEADERS["PRV"]))

            elif current_state == "INTERRUPT":
                if header == HEADERS["ACK"] and payload == HEADERS["INTR"]:
                    print(f"ACK received! Waiting for pass...")
                    current_state = "PAUSED"

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
    global current_state, received_payload, instruction_payload, previous_state, interrupt_code, interrupt_active, ldata_to_send, current_result, desired_result

    while 1:
        await send_event.wait()
        send_event.clear()
        try:
            print(f"\nCurrent State: {current_state}\n")
            if current_state == "INTERRUPT":
                interrupt_message = format_message(HEADERS["INTR"], interrupt_code)
                await websocket.send(interrupt_message)

            elif current_state == "SENDING":
                syn_message = format_message(HEADERS["SYN"])
                await websocket.send(syn_message)
                print(f"Trying to start data transfer...")
                ack_received = await websocket.recv()
                header, payload, _ = parse_message(ack_received)

                if header == HEADERS["ACK"] and payload == HEADERS["SYN"]:
                    print(f"ACK received! Starting data transfer...")
                    await send_data(websocket)

            elif current_state == "NEXT":
                next_message = format_message(HEADERS["NEXT"], current_result)
                await websocket.send(next_message)
                print(f"Sent next message...")

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

# Helper Function to send data
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
    global current_state, received_payload, instruction_payload, previous_state, interrupt_code, interrupt_active, ldata_to_send, send_next

    while True:
        if (interrupt_active):
            previous_state = current_state
            current_state = "INTERRUPT"
            interrupt_active = False
            print("Interrupt Active!")
            asyncio.run_coroutine_threadsafe(set_send(), loop)


        elif (ldata_to_send):
            instruction_payload = "Quando autem elevatum est cor eius, et spiritus illius obfirmatus est ad superbiam, depositus est de solio regni sui, et gloria eius ablata est et a filiis hominum eiectus est, sed et cor eius cum bestiis positum est, et cum onagris erat habitatio eius: foenum quoque ut bos comedebat, et rore caeli corpus eius infectum est, donec cognosceret quod potestatem haberet Altissimus in regno hominum: et quemcumque voluerit, suscitabit super illud."  # Data to be sent to central
            current_state = "SENDING"
            ldata_to_send = False
            asyncio.run_coroutine_threadsafe(set_send(), loop)


        elif (send_next):
            current_state = "NEXT"
            send_next = False
            asyncio.run_coroutine_threadsafe(set_send(), loop)
        
        else:
            pass

        time.sleep(0.5)

def keyword_checker(sentence: str):
    """
    Checks if a sentence contains specific keywords and returns a number based on the keyword found.
    """
    keywords = {
        "finely": "finely_dice",
        "roughly": "roughly_slice",
        "slice": "slice",
        "blonde": "blonde",
        "golden": "golden",
        "caramelize": "caramelized"
    }
    
    for word, value in keywords.items():
        if word in sentence.lower():  # Case insensitive match
            return value
    
    return ""  # Return 0 if no keyword is found

# Start WebSocket server
async def start_server():
    async with websockets.serve(websocket_handler, "localhost", 8765):
        print("Server Running!")

        # Start send_cases in a separate thread
        loop = asyncio.get_event_loop()
        cases_thread = threading.Thread(target=send_cases, args=(loop,), daemon=True)
        ML_thread = threading.Thread(target=ML_func, args=(), daemon=True)
        cases_thread.start()
        ML_thread.start()

        await asyncio.Future()  # run forever

# Machine Learning Detection
def ML_func():

    global step_index, desired_result, current_result, current_state, recipe_ready, received_payload

    while (current_state != "NEXT"):
        if((recipe_ready) and (received_payload != [])):
            desired_result = keyword_checker(received_payload[int(step_index)])

            if desired_result == "finely_dice" or desired_result == "roughly_slice" or desired_result == "slice": # onion cutting instruction
                print("Checking onion cut...")
                model_type = "onion_cut"
                run_ml_model(model_type)
            elif desired_result == "":
                pass
            else:
                model_type = "onion_cook"
                run_ml_model(model_type)

def run_ml_model(model_type):
    '''
    DANGER_CODES = {
    1: "FIRE",
    2: "CHOPPING TECHNIQUE",
    3: "LACERATION",
    4: "BURNS"
    }
    '''

    global current_result, interrupt_active, interrupt_code, step_index, current_state, previous_state, send_next, received_payload

    print(f"Step Index: {int(step_index)}")
    print(f"Current Step: {received_payload[int(step_index)]}")

    # conf_required = 0.08
    path = model_type + '.pt'
    model = torch.hub.load('yolov5', 'custom', path=path, source='local', verbose=False)
    model.conf = 0.4
    model.eval()
    
    extra_models = {}
    if model_type == "onion_cook":
        extra_models["fire"] = torch.hub.load('yolov5', 'custom', path="fire.pt", source='local', verbose=False)
    elif model_type == "onion_cut":
        extra_models["bloodstain"] = torch.hub.load('yolov5', 'custom', path="bloodstain.pt", source='local', verbose=False)
        extra_models["lacerations"] = torch.hub.load('yolov5', 'custom', path="lacerations.pt", source='local', verbose=False)
        extra_models["knife_safety"] = torch.hub.load('yolov5', 'custom', path="knife_safety.pt", source='local', verbose=False)
    
    for key in extra_models:
        extra_models[key].conf = 0.60
        extra_models[key].eval()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        exit()

    frame_count = 0
    previous_class = None

    current_step = copy.deepcopy(step_index)
    
    try:
        while (current_state != "NEXT"):

            ret, frame = cap.read()
            if not ret:
                break

            interrupt_active = False
            interrupt_code = None
            current_result = None
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model(rgb_frame)
            
            extra_results = {}
            for key in extra_models:
                extra_results[key] = extra_models[key](rgb_frame)

            if((current_step != step_index)): # if moved on, move on
                print("Moved On!")
                break
            
            for det in results.xyxy[0]:
                print(f"Current Model: {model_type}")

                x1, y1, x2, y2, conf, cls = det
                label = f"{results.names[int(cls)]} {conf:.2f}"
                class_name = label.split(" ")[0]
                print(f"{class_name}\n")
                confidence = float(label.split(" ")[1])
                
                if model_type == 'onion_cut':
                    if class_name == previous_class and confidence > 0.15:
                        frame_count += 1
                    else:
                        frame_count = 0
                    previous_class = class_name
                    if frame_count > 5:
                        current_result = class_name
                        print(f"Onion cut type: {class_name}")
                        break
                
                if model_type == 'onion_cook':
                    if class_name == previous_class and confidence > 0.15:
                        frame_count += 1
                    else:
                        frame_count = 0
                    previous_class = class_name
                    if frame_count > 5:
                        current_result = class_name
                        print(f"Onion cook type: {class_name}")
                        break
                
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if(current_result == desired_result):
                send_next = True
                time.sleep(0.5)
                break
            
            for key in extra_results:
                for det in extra_results[key].xyxy[0]:
                    x1, y1, x2, y2, conf, cls = det
                    label = f"{extra_results[key].names[int(cls)]} {conf:.2f}"
                    class_name = label.split(" ")[0]

                    if class_name == "fire":
                        if(current_state != "INTERRPUT" and current_state != "PAUSED"):
                            interrupt_active = True
                            interrupt_code = 1
                            print("WARNING: fire!")

                    if class_name == "lacerations" or class_name == "bloodstains":
                        if(current_state != "INTERRPUT" and current_state != "PAUSED"):
                            interrupt_active = True
                            interrupt_code = 3
                            print("WARNING: injury!")
                    
                    if class_name == "unsafe":
                        frame_count += 1
                    else:
                        frame_count = 0
                    if frame_count > 5:
                        if(current_state != "INTERRPUT" and current_state != "PAUSED"):
                            interrupt_active = True
                            interrupt_code = 2
                            print("WARNING: unsafe knife handling")
            
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    except KeyboardInterrupt:
        print("\nChange ML model type")
    
    cap.release()
    cv2.destroyAllWindows()
                    
# return function
def run_diagnostic():

    global current_result, desired_result, send_next

    with lock:
        print(f"desired: {desired_result}")
        print(current_result)

    return 
            
# main
if __name__ == "__main__":

    # Run WebSocket server
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("\nStopping WebSocket server.")