# Imports
import threading
import time
import serial

# Configuration
MAX_MESSAGES = 1 # maximum amount of messages that can be stored inside the box
PASSWORD = "purple" # admin password
ser = serial.Serial('/dev/ttyUSB0', 9600)

messages = {} # dictionary for storing messages
times = {} # dictionary for storing countdown timers

def sudo(command):
    password_input = input("[sudo] password for administrator: ")
    if password_input == PASSWORD:
        if command.startswith("sudo viewmessage"):
            message_to_read = command.split()[2]
            print(message_to_read)
            # TODO: Print message being searched by user and the time until release
            print(messages.get(int(message_to_read)))
        # TODO: Add more sudo commands
        #  eject {message number}
        #  time set {message number}
        #  time remaining {message number}
        #  time subtract {message number}
        #  time add {message number}
        #  journal {message_number} (shows actively updating countdown in terminal)
        #  serial freeze
        #  serial unfreeze
        #  serial write {input}

def input_message():
    message = input("Enter a message: ")
    if message.startswith("sudo "):
        command = message
        sudo(command)
    else:
        time_to_store = input("Enter how long you want to store your message for (Format as #w #d #h #min #s: ")
        return message, time_to_store

# TODO: Create countdown timers that write to serial, prefixed by their message number for display on the LCD
#       that wil change the time it is showing between messages every 5 seconds. Upon timer end, write
#       eject {message number} to serial

def main():
    input_message()

main()

