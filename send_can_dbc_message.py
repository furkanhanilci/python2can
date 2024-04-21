import cantools
from can.message import Message
import can

db = cantools.db.load_file('your dbc file path here.dbc') # Load the DBC file

msg = db.get_message_by_name('AUTO_SPEED_CONTROL') # Get the message by name

msg_data = msg.encode({'auto_acc_pedal_position':100,
                       'auto_drive_activation_command':0,
                       'speed_ramp_command':1,
                       'speed_KP_command':1,
                       'speed_KI_command':1,
                       'target_speed_command':1}) # Encode the message data



bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)  # Create a bus instance
msg = can.Message(arbitration_id=msg.frame_id, data=msg_data, is_extended_id=False) # Create a message instance


try:
    bus.send(msg) # Send the message
    print("Message sent on {}".format(bus.channel_info)) # Print the message sent

except can.CanError: # If there is a CAN error
     print("Message NOT Sent") # Print message not sent



