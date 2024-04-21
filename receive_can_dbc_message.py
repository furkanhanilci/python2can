import cantools
from can.message import Message
import can

db = cantools.db.load_file('your dbc file path here.dbc') # Load the DBC file

print("CAN Messages Receiving Process İnitialized.") # Print the process initialized

try: # Try to receive the message

    bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000) # Create a bus instance
    while True:
        message = bus.recv() # Receive the message
        print(db.decode_message(message.arbitration_id,message.data)) # Print the received message
    
except: # If there is a CAN error
    print("Process Has Done!") # Print the process has done