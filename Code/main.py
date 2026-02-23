# Imports
import threading
import time
import serial

# Config
MAX_MESSAGES = 1 # maximum amount of messages that can be stored inside the box
available_slots = list(range(MAX_MESSAGES)) # list of available slots

PASSWORD = "purple" # admin password
BAUD_RATE = 9600
PORT = "/dev/ttyACM0"

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
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
                with lock:
                    eject(message_number)
            except ValueError:
                print("{eject}: message number must be an integer")

        # Had Claude Sonnet 4.5 make the sudo serial commands because I wanted to test my wiring ASAP
        # sudo serial --freeze
        if command.startswith("sudo serial --freeze") or command.startswith("sudo serial -f"):
            # TODO: Implement serial freeze logic
            # This should pause the countdown_thread from sending serial commands
            print("Serial freeze not yet implemented")

        # sudo serial --unfreeze
        if command.startswith("sudo serial --unfreeze") or command.startswith("sudo serial -uf"):
            # TODO: Implement serial unfreeze logic
            # This should resume the countdown_thread sending serial commands
            print("Serial unfreeze not yet implemented")

        # sudo serial --write {input}
        if command.startswith("sudo serial --write") or command.startswith("sudo serial -w"):
            if command.startswith("sudo serial --write"):
                serial_input = command[len("sudo serial --write"):].strip()
            else:  # sudo serial -w
                serial_input = command[len("sudo serial -w"):].strip()

            if not serial_input:
                print("{serial --write}: missing required argument: input")
                return

            if ser:
                ser.write(f"{serial_input}\n".encode("utf-8"))
                print(f"Sent to serial: {serial_input}")
            else:
                print("No serial connection available")

        # # sudo time --{command} {message number}
        # # VERY UNFINISHED, MOSTLY JUST COPIED FROM sudo eject
        # if command.startswith("sudo time"):
        #     parts = command.split()
        #     if len(parts) < 3:
        #         print("{time}: missing required argument(s)")
        #         return
        #         # add more specific error, such as missing message number and/or missing command argument
        #     if command.startswith("sudo time set"):
        #         try:
        #             message_number = int(parts[2])  # Convert to int
        #             time_to_set = int(parts[3])
        #             with lock:  # Need lock since eject modifies shared data
        #                 # message number time remaining =
        #         except ValueError:
        #             print("{time}: message number must be an integer")



        # TODO: Add more sudo commands
        #  time --set {message number}
        #  time --remaining {message number} (or -r)
        #  time --subtract {message number} (or -s)
        #  time --add {message number} (or -a)
        #  journal {message_number} (shows actively updating countdown in terminal)
        #  serial --freeze (or -f)
        #  serial --unfreeze (or -uf)
        #  serial --write {input} (or -w)


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
    ejecting_message = None
    eject_display_until = 0

    while True:
        current_time = time.time()

        with lock:
            expired = []
            for message_id, message_data in messages.items():
                remaining = message_data["end_time"] - current_time

                if remaining <= 0:
                    expired.append(message_id)

            for message_id in expired:
                eject(message_id)
                ejecting_message = message_id
                eject_display_until = current_time + 5  # Display for 5 seconds

            # Display ejection message for 5 seconds
            if ejecting_message is not None and current_time < eject_display_until:
                if ser:
                    ser.write(f"[ejecting] {ejecting_message}\n".encode("utf-8"))
            # Display no messages waiting
            elif not messages:
                if ser:
                    ser.write(f"[no_messages]\n".encode("utf-8"))
            # Display countdown
            elif messages:
                active_message_numbers = list(messages.keys())
                if active_message_numbers:
                    # Switch to next message every 5 seconds
                    if current_time - last_display_switch >= 5:
                        display_index = (display_index + 1) % len(active_message_numbers)
                        last_display_switch = current_time

                    # Send update every second for current message
                    message_id = active_message_numbers[display_index % len(active_message_numbers)]
                    remaining = messages[message_id]["end_time"] - current_time

                    if ser:
                        ser.write(f"[display] {message_id} {int(remaining)}\n".encode("utf-8"))

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
