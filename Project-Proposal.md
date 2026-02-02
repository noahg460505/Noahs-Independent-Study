# Project Proposal
## Goal
   My goal for this project is to make an interactive "Message Time Capsule" box that uses a Raspberry Pi to take input from a keyboard and print it via a thermal printer into a compartment in a box. The user inputs a time after they input their message for how long the message will stay in the box before the message compartment is ejected out of the box using a motor. Message input will be displayed as it is being typed, and the time until the message is released will also be displayed.
   
   ### Key Design Decisions
   - **Single compartment for v1**: Start simple with one slot, could possibly expand to multiple compartments as an extension
   - **Manual drawer reset**: Drawer ejects automatically when timer expires, but the user manually inserts it back in to reset. I think having the drawer fully eject out of the box would be funny, plus it'll likely be easier to implement than a retraction mechanism.
   - **Arduino for motor control**: Using Arduino Uno to handle motor/servo control and drive the LCD display, while the Pi manages the thermal printer, timers, and keyboard input. The Pi tells the Arduino what to display and when to activate the motor.
   - **Character LCD display**: LCD will alternate between showing countdown and status messages

## Initial Bill of Materials
### Already Have:
- MDF sheets or the birch sheets we have
- Gearmotor
- Filament for 3D printing
- Raspberry Pi (Probably a 3B+) + MicroSD Card + Power Supply
- Arduino Uno
- Various Wires
- LCD Display
- Servo
- 12V Power Supply
- Keyboard
- USB-A to MicroUSB Cable (Pi to Arduino)
- LEDs

### Need to Obtain:
- Thermal Printer + Thermal Paper

## Possible Extensions
Possible extensions for if I finish the project early:

### Realistic Extensions
- **Multiple compartments**: Expand to 4-slot carousel or drawer system with individual timers
- **Sound effects/LEDs**: Add audio/visual feedback for countdown milestones and release events
- **Early retrieval system**: Override to retrieve messages before timer expires using a password
- **Motor driver board**: Replace Arduino with direct Pi motor control

### Ambitious Extensions
- **Touchscreen interface**: Replace keyboard + character LCD with a touchscreen
- **Smaller form factor**: Miniaturize the design once functionality is proven

### Stretch Goals
- **Remote web interface**: Remote monitoring of compartment status and countdowns
