from bluezero import peripheral
import time
import threading


""""" 

Setup (Variables, etc.) DONE!!!

"""""

# BLE service and characteristic UUIDs
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"

# Variables
current_state = "IDLE"  # States: IDLE, RECEIVING, SENDING, INTERRUPT, PAUSED
received_payload = []      # Buffer to store received recipe steps
instruction_payload = ""   # Data to be sent to central
ack_received = False       # Flag for ACK status
interrupt_active = False   # Flag to indicate an active interrupt
interrupt_code = ""

HEADERS = {
    "SYN": 0x10,
    "ACK": 0x01,
    "DATA": 0x11,
    "FIN": 0x20,
    "RST": 0x30,
    "HEARTBEAT": 0x40,
    "INTR": 0x60,
    "PASS": 0x70,
    "INVALID": 0xFF
}

DANGER_CODES = {
    "FIRE": 0x46495245,
    "KNIFE DISTANCE": 0x4B4E4946452044495354414E4345,
    "BLEEDING":0x424C454544494E47,
    "HOT PAN": 0x484F542050414E,
    "SLIPS": 0x534C495053
}

# Helper function to format messages into 32-bit packets
def format_message(header, payload):
    # Header: 1 byte for type, 1 byte reserved, 2 bytes for sequence/offset
    # Payload: 28 bytes
    header_bytes = header.to_bytes(1, 'big') + b'\x00' + (len(payload).to_bytes(2, 'big'))
    payload_bytes = payload.ljust(28, b'\x00')[:28]  # Pad or truncate payload to 28 bytes
    return header_bytes + payload_bytes

def parse_message(packet):
    header = packet[0]
    payload = packet[4:].rstrip(b'\x00')
    return header, payload

def send_ack(msg_type):
    global ack_received
    ack_packet = format_message(header=HEADERS["ACK"], payload=msg_type.to_bytes(1, 'big'))
    return ack_packet


""""" 

Peripheral-Initiated Steps (Indicators)

"""""

def send_indication(data):
    global ble_peripheral
    characteristic = ble_peripheral.find_characteristic(CHARACTERISTIC_UUID)
    if characteristic:
        characteristic.indicate(data)
        print(f"Indication sent: {data}")

def send_data():
    global instruction_payload, current_state

    # Break data into chunks and send
    data = instruction_payload.encode('utf-8')  # Convert the data to bytes
    chunk_size = 28  # Maximum payload size
    sequence = 0  # Sequence number for the packets

    while data:
        
        chunk, data = data[:chunk_size], data[chunk_size:]

        message = format_message(header=HEADERS["DATA"], payload=chunk)

        # Send the message as an indication
        send_indication(message)
        print(f"Sent chunk {sequence}: {chunk.decode('utf-8')}")
        sequence += 1
        time.sleep(0.1)

    # Send the FIN header to indicate the end of the transmission
    fin_message = format_message(header=HEADERS["FIN"], payload=b"")
    send_indication(fin_message)
    print("All data sent. Sent FIN message.")
    current_state = "IDLE"


""""" 

Central-Initiated Steps (Write_callback) DONE!!!!

"""""

def write_callback(value):
    global current_state, received_payload, ack_received, instruction_payload, interrupt_active

    header, payload = parse_message(value)

    if current_state == "IDLE" and header == HEADERS["SYN"]:   ## Ready to receive data
        print("Central initiating data transfer.")
        current_state = "RECEIVING"
        return send_ack(HEADERS["SYN"])

    elif current_state == "RECEIVING": ## Currently receiving data chunks
        if header == HEADERS["FIN"]:
            print("Central indicating end of payload.")
            current_state = "IDLE"
            return send_ack(HEADERS["FIN"])
        else:
            received_payload.append(payload.decode('utf-8'))
            print(f"Received chunk: {payload.decode('utf-8')}")
            return send_ack(HEADERS["DATA"])
           
    elif current_state == "PAUSED" and header == HEADERS["PASS"]: ## Receive PASS message once danger averted
        print("Pass message received from central. Resuming operation.")
        current_state = "IDLE"
        return send_ack(HEADERS["PASS"])
    
    elif current_state == "PAUSED" and header == HEADERS["ACK"] and payload == HEADERS["INTR"]: ## Interrupt acked by central
        print("Interrupt acked by central.")
        return send_ack(HEADERS["ACK"])
    
    elif current_state == "IDLE" and header == HEADERS["ACK"] and payload == HEADERS["FIN"]: ## FIN indicator acknowledged
        print("Central acknowledged finish message.")
        current_state = "IDLE"
        return send_ack(HEADERS["ACK"])
    
    elif current_state == "IDLE" and header == HEADERS["ACK"] and payload == HEADERS["SYN"]: ## SYN indicator acknowledged
        print("Central acknowledged start of peripheral communication.")
        ack_received = True
        current_state = "SENDING"
        return send_ack(HEADERS["ACK"])
    
    elif header == HEADERS["RST"]: ## RST message
        print("Resetting to idle state.")
        current_state = "IDLE"
        received_payload = []
        return send_ack(HEADERS["RESET"])
    
    else:
        print(f"Unexpected value: {value}")
        return format_message(HEADERS["INVALID"], b"INVALID")

""""" 

Heartbeats (Read_callbacks) DONE!!

"""""

def read_callback():
    return send_ack(HEADERS["HEARTBEAT"])


""""" 

Interrupt Thread (Indicators) DONE!!!

"""""

def handle_interrupt():
    global current_state, interrupt_code, interrupt_active

    while True:
        if current_state == "INTERRUPT" and interrupt_active:
            interrupt_packet = format_message(header=HEADERS["INTR"], payload=DANGER_CODES[interrupt_code])
            send_indication(interrupt_packet)
            current_state = "PAUSED"
            
        return


""""" 

BLE Service Publishing DONE!!!

"""""

ble_peripheral = peripheral.Peripheral(
    adapter_address="2C:CF:67:77:45:BF",
    local_name="AIpron",
)

ble_peripheral.add_service(srv_id=1, uuid=SERVICE_UUID, primary=True)
ble_peripheral.add_characteristic(
    srv_id=1,
    chr_id=1,
    uuid=CHARACTERISTIC_UUID,
    flags=['read', 'write', 'indicate'],
    value=b"",
    read_callback=read_callback,
    write_callback=write_callback,
    notifying=False
)

# Start advertising the BLE peripheral
print("Starting BLE advertising...")
ble_peripheral.publish()
print("BLE peripheral running. Waiting for connection...")

# Start the interrupt in a separate thread
interrupt_thread = threading.Thread(target=handle_interrupt, daemon=True)
interrupt_thread.start()

try:
    while True:
        time.sleep(1)

        if current_state == "SENDING":

            if not ack_received:
                syn_message = format_message(header=HEADERS["SYN"], payload=b"")
                send_indication(syn_message)
                current_state == "IDLE"
            else:
                send_data()
                ack_received = False

except KeyboardInterrupt:
    print("\nStopping BLE peripheral.")
