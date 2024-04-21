import can
import cantools
import time
import pygame
import os

# Initialize CAN bus
os.system("sudo modprobe peak_usb") # Load the peak_usb driver
os.system("sudo modprobe peak_pci") # Load the peak_pci driver
os.system("sudo ip link set vcan0 up type can bitrate 500000")  # Set up the vcan0 interface
can_bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)   # Create a bus instance

pygame.init()   # Initialize pygame
joystick = pygame.joystick.Joystick(0)  # Initialize the joystick
joystick.init() # Initialize the joystick

# Load DBC file
db = cantools.database.load_file(r'dbc/rbf.dbc')
message_name_298 = 'CommandMessage' # Define the message name
message_298 = db.get_message_by_name(message_name_298)  # Get the message by name

db = cantools.database.load_file(r'dbc/son_dbc.dbc')    # Load the DBC file
message_name_301 = 'Autonomous_Driving'   # Define the message name
message_301 = db.get_message_by_name(message_name_301)  # Get the message by name


def map_joystick_thumb_right(joystick_value):   # Define the function
    joystick_min = -1   # Define the minimum value of the joystick
    joystick_max = 1    # Define the maximum value of the joystick
    angle_min = -75    # Define the minimum angle
    angle_max = 75   # Define the maximum angle
    mapped_angle = (joystick_value - joystick_min) / (joystick_max - joystick_min) * (angle_max - angle_min) + angle_min # Map the joystick value to the angle
    return max(angle_min, min(angle_max, mapped_angle)) # Return the mapped angle


def map_joystick_thumb_left(joystick_value):    # Define the function
    joystick_min = -1   # Define the minimum value of the joystick
    joystick_max = 1    # Define the maximum value of the joystick
    angle_min = -700    # Define the minimum angle
    angle_max = 700   # Define the maximum angle
    mapped_angle = (joystick_value - joystick_min) / (joystick_max - joystick_min) * (angle_max - angle_min) + angle_min # Map the joystick value to the angle
    return max(angle_min, min(angle_max, mapped_angle)) # Return the mapped angle


def switch_gear(gear_mode):   # Define the function
    """
    Switches gears based on the gear mode.
    """
    gear_values = {
        0: (1, 0, 0),  # Drive
        1: (0, 1, 0),  # Neutral
        2: (0, 0, 1),  # Reverse
    }
    return gear_values.get(gear_mode, (0, 1, 0))  # Default to Neutral if gear mode is not recognized


# Initialize variables
speed_fh = 0    # Define the speed
steer_wh_angle_fh = 0   # Define the steering angle
target_speed = 0    # Define the target speed
drive_mode = 0  # Define the drive mode
button_info = 1 # Define the button info
robeff_reset_command = 1    # Define the robeff reset command
exitprogram = 0 # Define the exit program
gear_mode = 0   # Define the gear mode
# Main loop
while True:
    for event in pygame.event.get():    # Get the event
        if event.type == pygame.QUIT:   # If the event type is quit
            pygame.quit()   # Quit pygame
            quit()  # Quit the program

    joystick_left = joystick.get_axis(0)    # Get the joystick axis
    joystick_right = joystick.get_axis(2)   # Get the joystick axis

    if joystick.get_button(0) == 1: # If the button is pressed
        drive_mode = 3  # Set the drive mode to 3
        button_info = 0 # Set the button info to 0
    elif joystick.get_button(3) == 1:   # If the button is pressed
        drive_mode = 3  # Set the drive mode to 3
        button_info = 1 # Set the button info to 1
        robeff_reset_command = 0    # Set the robeff reset command to 0
    elif joystick.get_button(1) == 1:   # If the button is pressed
        button_info = 0 # Set the button info to 0
        drive_mode = 0  # Set the drive mode to 0
        steer_wh_angle_eby = 0  # Set the steering angle to 0
    # exitprogram = 1
    elif joystick.get_button(4) == 1:   # If the button is pressed
        robeff_reset_command = 1    # Set the robeff reset command to 1
    elif joystick.get_button(6) == 1:   # If the button is pressed
        target_speed = max(0, target_speed - 1)   # Set the target speed
        time.sleep(0.01)    # Sleep for 0.01 seconds
    elif joystick.get_button(7) == 1:   # If the button is pressed
        target_speed += 1   # Increment the target speed
        time.sleep(0.01)    # Sleep for 0.01 seconds
    elif joystick.get_button(11) == 1:  # If the button is pressed
        gear_mode += 1  # Increment the gear mode
        if gear_mode > 2:   # If the gear mode is greater than 2
            gear_mode = 0   # Set the gear mode to 0
        time.sleep(0.5) # Sleep for 0.5 seconds
    elif joystick.get_button(10) == 1:  # If the button is pressed
        exit(1)   # Exit the program

    speed_fh = target_speed / (3.6)   # Calculate the speed

    joystick_map = joystick_right if button_info == 0 else joystick_left    # Map the joystick value
    mapped_angle = map_joystick_thumb_left(joystick_map) if button_info == 0 else map_joystick_thumb_right(joystick_map)    # Map the joystick value
    steer_wh_angle_fh = mapped_angle   # Set the steering angle

    data_298 = message_298.encode({
        'ControlMode': 0,
        'ReferenceDutyCycle': 0,
        'SetSteeringAngle': steer_wh_angle_fh,
        'ResetCommand': robeff_reset_command
    })  # Encode the message data
    can_msg = can.Message(arbitration_id=0x298, data=data_298, is_extended_id=False)    # Create a message instance
    can_bus.send(can_msg, 0.01) # Send the message

    drive_gear, neutral_gear, reverse_gear = switch_gear(gear_mode)   # Switch the gear
    data_301 = message_301.encode({
        'speed_ramp_command': 1,
        'speed_KP_command': 25,
        'speed_KI_command': 1,
        'command_brake_acc': 0,
        'DriveMode': drive_mode,
        'command_long_vel': speed_fh,
        'Drive': drive_gear,
        'Neutral': neutral_gear,
        'Reverse': reverse_gear,
    })  # Encode the message data

    can_msg = can.Message(arbitration_id=0x301, data=data_301, is_extended_id=False)    # Create a message instance
    can_bus.send(can_msg, 0.01) # Send the message

    """
    print ("gear_mode =",gear_mode)
    print ("drive_gear =",drive_gear)
    print ("neutral_gear =",neutral_gear)
    print ("reverse_gear =",reverse_gear)
    """

    """
    print('vel:', speed_fh)
    print('steer_angle:', steer_wh_angle_fh)
    print('drivemode:', drive_mode)
    print(format(can_bus.channel_info))
    print(f"Joystick X: {joystick_map}, Mapped Angle: {steer_wh_angle_fh}")
    """

    if robeff_reset_command == 1:   # If the robeff reset command is 1
        robeff_reset_command = 0    # Set the robeff reset command to 0
    if exitprogram == 1:    # If the exit program is 1
        break   # Break the loop
    time.sleep(0.01)    # Sleep for 0.01 seconds