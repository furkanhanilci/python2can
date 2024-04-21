import cantools
import os
from can.message import Message


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))    # Get the script directory
INPUT_DBC_PATH = os.path.join(SCRIPT_DIR, 'autonomous_atak.dbc')    # Get the input dbc path
OUTPUT_DBC_PATH = os.path.join(SCRIPT_DIR, 'autonomous_atak_dbc_output.dbc')    # Get the output dbc path
print("Loading DBC database from '{}'.".format(INPUT_DBC_PATH))   # Print the loading DBC database
db = cantools.db.load_file(INPUT_DBC_PATH)  # Load the DBC file

#print the content od dbc
print(db)

#print particular message in the dbc
can_msg = db.get_message_by_name('AUTO_SPEED_CONTROL')
print("can message :",can_msg)


can_msg_data = can_msg.encode({'auto_acc_pedal_position':100,'auto_drive_activation_command':1, 'speed_ramp_command':1, 'speed_KP_command':1, 'speed_KI_command':1, 'target_speed_command':1})  # Encode the message data
print(can_msg_data) # Print the message data


with open(OUTPUT_DBC_PATH, 'w', newline="\r\n") as fout:    # Open the output dbc path
    fout.write(str(db))   # Write the DBC file
    fout.write("\n")    # Write a new line
    fout.write(str(can_msg_data))   # Write the message data