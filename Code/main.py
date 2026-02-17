# Imports
import threading
import time
import serial

# Config
MAX_MESSAGES = 1 # maximum amount of messages that can be stored inside the box
available_slots = list(range(MAX_MESSAGES)) # list of available slots

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

        # sudo viewmessage {message number}
        if command.startswith("sudo viewmessage"):
            parts = command.split()
            if len(parts) < 3:
                print("{viewmessage}: missing required argument: message number")
                return
            try:
                message_number = int(parts[2])
                print(f"Message Number: {message_number}")
                with lock:
                    message_data = messages.get(int(message_number))
                    if message_data:
                        remaining = message_data["end_time"] - time.time()
                        print(f"Message: {message_data['text']}")
                        print(f"Time remaining: {remaining:.1f} seconds")
                    else:
                        print("Message not found")
            except ValueError:
                print("{viewmessage}: message number must be an integer")

        # sudo eject {message number}
        if command.startswith("sudo eject"):
            parts = command.split()
            if len(parts) < 3:
                print("{eject}: missing required argument: message number")
                return
            try:
                message_number = int(parts[2])  # Convert to int
                with lock:  # Need lock since eject modifies shared data
                    eject(message_number)
            except ValueError:
                print("{eject}: message number must be an integer")


        # TODO: Add more sudo commands
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
        slot = messages[message_number]["slot"]
        if ser:
            ser.write(f"[eject] {slot}\n".encode("utf-8"))
        print("\nEjected message #" + str(message_number))
        available_slots.append(slot)  # open up slot for new message
        available_slots.sort()  # sort the slots to keep them in the correct order
        del messages[message_number]  # remove message from dictionary

def countdown_thread():
    display_index = 0
    last_display_switch = time.time()

    while True:
        current_time = time.time()

        with lock:
            expired = []
            for message_number, message_data in messages.items():
                remaining = message_data["end_time"] - current_time

                if remaining <= 0:
                    expired.append(message_number)

            for message_number in expired:
                eject(message_number)

            if messages and (current_time - last_display_switch >= 5):
                active_message_numbers = list(messages.keys())
                if active_message_numbers:
                    display_index = display_index % len(active_message_numbers)
                    message_number = active_message_numbers[display_index]

                    if ser:
                        ser.write(f"[display] {message_number}\n".encode("utf-8"))

                    display_index = (display_index + 1) % len(active_message_numbers)
                    last_display_switch = current_time
        time.sleep(1)

def parse_time_input(time_input):
    try:
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
                return None
    except (ValueError, IndexError):
        print("Invalid Time Input - could not parse numbers")
        return None


def input_message():
    message = input("Enter a message: ")
    if message.startswith("sudo "):
        command = message
        sudo(command)
        return None
    else:
        with lock:
            if not available_slots:  # check for available slots
                # Find the message that is closest to being ejected
                soonest_time = min(message_data["end_time"] for message_data in messages.values())
                remaining = soonest_time - time.time()

                print(f"All {MAX_MESSAGES} slot(s) full. Next slot available in {remaining:.1f} seconds.")
                return None

            slot = available_slots.pop(0)  # pick first available slot

        time_input = input("Enter how long you want to store your message for (Format as #yr #mo #w #d #h #mi #s): ")
        time_to_store = parse_time_input(time_input)

        if time_to_store is None:
            # Return slot to available slots if parsing failed
            with lock:
                available_slots.append(slot)
                available_slots.sort()
            return None

        with lock:
            # Use slot number as message ID instead of separate counter
            messages[slot] = {
                "text": message,
                "end_time": time.time() + time_to_store,
                "slot": slot
            }
        return message, time_input, slot

def main():
    # start countdown thread
    thread = threading.Thread(target=countdown_thread, daemon=True)
    thread.start()

    while True:
        result = input_message()
        if result is None:
            continue

main()
