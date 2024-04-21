import os
import cantools
from can.message import Message

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
INPUT_DBC_PATH = os.path.join(SCRIPT_DIR, 'your input dbc file path here.dbc')
OUTPUT_DBC_PATH = os.path.join(SCRIPT_DIR, 'your output dbc file path here.dbc')

# Read the DBC.
print("Loading DBC database from '{}'.".format(INPUT_DBC_PATH))
db = cantools.db.load_file(INPUT_DBC_PATH)

# Get a message to manipulate.
can_msg = db.get_message_by_name('your message name here')

# Manipulate the message frame id.
print("Input frame id: ", hex(can_msg.frame_id))
can_msg.frame_id = 0x234
print("Output frame id:", hex(can_msg.frame_id))

print("Writing modified DBC database to '{}'.".format(OUTPUT_DBC_PATH))

with open(OUTPUT_DBC_PATH, 'w', newline="\r\n") as fout:
    fout.write(db.as_dbc_string())
