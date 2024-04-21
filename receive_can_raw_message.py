import can

can_bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)              


while True:
        try: # Try to receive the message
            message = can_bus.recv() # Receive the message
            print(message) # Print the received message

        except can.CanError: # If there is a CAN error
            print("Message NOT Received")   # Print message not received