# Imports
import threading
import time
import serial

# Configuration
MAX_MESSAGES = 1 # maximum amount of messages that can be stored inside the box
PASSWORD = "purple" # admin password
BAUD_RATE = 9600
PORT = "/dev/ttyUSB0"

try:
    ser = serial.Serial(PORT, BAUD_RATE)
except serial.SerialException:
    ser = None
    print("No serial connected.")

messages = {} # dictionary for storing messages
times = {} # dictionary for storing countdown timers
message_counter = 0
lock = threading.Lock()

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


def eject(message_number):
    if message_number in messages:
        if ser:  # CHANGED: was serial.Serial.write
            ser.write(f"[eject] {message_number}\n".encode("utf-8"))
        print("Ejected message #" + str(message_number))

def countdown_thread():
    display_index = 0
    last_display_switch = time.time()

    while True:
        current_time = time.time()

        with lock:
            expired = []
            for msg_id, msg_data in messages.items():
                remaining = msg_data["end_time"] - current_time

                if remaining <= 0:
                    eject(msg_id)
                    expired.append(msg_id)

            for msg_id in expired:
                del messages[msg_id]

            if messages and (current_time - last_display_switch >= 5):
                active_ids = list(messages.keys())
                display_index = (display_index + 1) % len(active_ids)
                msg_id = active_ids[display_index]

                if ser:
                    ser.write(f"[display] {msg_id}\n".encode("utf-8"))

                last_display_switch = current_time

        time.sleep(1)

def parse_time_input(time_input):
    translation_table = str.maketrans("", "", "abcdefghijklmnopqrstuvwxyz")
    stripped_time = time_input.translate(translation_table).split(" ")
    time_list_length = len(stripped_time)
    match time_list_length:
        case 1:
            seconds = int(stripped_time[-1])
            time_to_store = seconds
            return time_to_store
        case 2:
            seconds = int(stripped_time[-1])
            minutes_to_seconds = (int(stripped_time[-2])) * 60
            time_to_store = seconds + minutes_to_seconds
            return time_to_store
        case 3:
            seconds = int(stripped_time[-1])
            minutes_to_seconds = (int(stripped_time[-2])) * 60
            hours_to_seconds = (int(stripped_time[-3])) * 60 * 60
            time_to_store = seconds + minutes_to_seconds + hours_to_seconds
            return time_to_store
        case 4:
            seconds = int(stripped_time[-1])
            minutes_to_seconds = (int(stripped_time[-2])) * 60
            hours_to_seconds = (int(stripped_time[-3])) * 60 * 60
            days_to_seconds = (int(stripped_time[-4]))*24*60*60
            time_to_store = seconds + minutes_to_seconds + hours_to_seconds + days_to_seconds
            return time_to_store
        case 5:
            seconds = int(stripped_time[-1])
            minutes_to_seconds = (int(stripped_time[-2])) * 60
            hours_to_seconds = (int(stripped_time[-3])) * 60 * 60
            days_to_seconds = (int(stripped_time[-4])) * 24 * 60 * 60
            weeks_to_seconds = (int(stripped_time[-5]))*7*24*60*60
            time_to_store = seconds + minutes_to_seconds + hours_to_seconds + days_to_seconds + weeks_to_seconds
            return time_to_store
        case 6:
            seconds = int(stripped_time[-1])
            minutes_to_seconds = (int(stripped_time[-2])) * 60
            hours_to_seconds = (int(stripped_time[-3])) * 60 * 60
            days_to_seconds = (int(stripped_time[-4])) * 24 * 60 * 60
            weeks_to_seconds = (int(stripped_time[-5])) * 7 * 24 * 60 * 60
            months_to_seconds = (int(stripped_time[-6]))*30*24*60*60 # approximation, might fix later, idk
            time_to_store = seconds + minutes_to_seconds + hours_to_seconds + days_to_seconds + weeks_to_seconds + months_to_seconds
            return time_to_store
        case 7:
            seconds = int(stripped_time[-1])
            minutes_to_seconds = (int(stripped_time[-2])) * 60
            hours_to_seconds = (int(stripped_time[-3])) * 60 * 60
            days_to_seconds = (int(stripped_time[-4])) * 24 * 60 * 60
            weeks_to_seconds = (int(stripped_time[-5])) * 7 * 24 * 60 * 60
            months_to_seconds = (int(stripped_time[-6])) * 30 * 24 * 60 * 60  # approximation, might fix later, idk
            years_to_seconds = (int(stripped_time[-7]))*365*24*60*60
            time_to_store = seconds + minutes_to_seconds + hours_to_seconds + days_to_seconds + weeks_to_seconds + months_to_seconds + years_to_seconds
            return time_to_store
        case _:
            print("Invalid Time Input")
            main()
            return None


def input_message():
    global message_counter
    message = input("Enter a message: ")
    if message.startswith("sudo "):
        command = message
        sudo(command)
        return None
    else:
        time_input = input("Enter how long you want to store your message for (Format as #yr #mo #w #d #h #mi #s): ")
        with lock:
            message_counter += 1
            time_to_store = parse_time_input(time_input)
            messages[message_counter] = {
                "text": message,
                "end_time": time.time() + time_to_store,
                "slot": 0
            }
        return message, time_input, message_counter

def main():
    thread = threading.Thread(target=countdown_thread, daemon=True)
    thread.start()

    while True:
        result = input_message()
        if result is None:
            continue

main()

