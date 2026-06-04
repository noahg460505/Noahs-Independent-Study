#include <LiquidCrystal.h>
#include <Servo.h>

// LCD pins
const int rs = 13, en = 12, d4 = 11, d5 = 10, d6 = 9, d7 = 8;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Motor A (Cutter)
const int PWMA = 5;
const int AIN1 = 7;
const int AIN2 = 6;

// Servo (Ejector)
#include <Servo.h>
Servo ejectServo;
const int SERVO_PIN = A0;

// servo home and eject limits
const int SERVO_HOME = 20;   // locked
const int SERVO_EJECT = 0;   // open

String inputBuffer = "";

void setup() {
  lcd.begin(16, 2);
  lcd.print("Starting...");

  Serial.begin(9600);

  // Motor A setup (cutter)
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(PWMA, OUTPUT);

  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, LOW);
  analogWrite(PWMA, 0);

  // Servo setup
  ejectServo.attach(SERVO_PIN);
  ejectServo.write(SERVO_HOME);
  delay(500);
  ejectServo.detach();

  lcd.clear();
  lcd.print("Ready");
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();

    if (c == '\n') {
      processCommand(inputBuffer);
      inputBuffer = "";
    } else if (c != '\r') {
      inputBuffer += c;
    }
  }
}

void processCommand(String command) {
  command.trim();
  int firstSpace = command.indexOf(' ');

  // eject message
  if (command.startsWith("[eject]")) {
    if (firstSpace != -1) {
      int message_number = command.substring(firstSpace + 1).toInt();
      display("ejecting", message_number, 0);
      cutReceipt();
      eject(message_number);
    }
  }

  // display countdown
  else if (command.startsWith("[display]")) {
    if (firstSpace != -1) {
      String data = command.substring(firstSpace + 1);
      int secondSpace = data.indexOf(' ');

      if (secondSpace != -1) {
        int msg_id = data.substring(0, secondSpace).toInt();
        int remaining_seconds = data.substring(secondSpace + 1).toInt();
        display("countdown", msg_id, remaining_seconds);
      }
    }
  }

  // eject + display
  else if (command.startsWith("[ejecting]")) {
    if (firstSpace != -1) {
      int message_number = command.substring(firstSpace + 1).toInt();
      display("ejecting", message_number, 0);
      cutReceipt();
      eject(message_number);
    }
  }

  // no messages
  else if (command.startsWith("[no_messages]")) {
    display("no_messages", 0, 0);
  }

  // TEST EJECT
  else if (command.startsWith("[test_eject]")) {
    Serial.println("TEST: eject");
    display("ejecting", 999, 0);
    eject(999);
  }

  // TEST CUTTER
  else if (command.startsWith("[test_cut]")) {
    Serial.println("TEST: cutter");
    cutReceipt();
  }
}

void display(String mode, int msg_id, int remaining_seconds) {
  lcd.clear();
  lcd.setCursor(0, 0);

  if (mode == "countdown") {
    lcd.print("Msg #");
    lcd.print(msg_id);

    lcd.setCursor(0, 1);
    lcd.print(remaining_seconds);
  }
  else if (mode == "ejecting") {
    lcd.print("Ejecting Msg #");
    lcd.print(msg_id);
  }
  else if (mode == "no_messages") {
    lcd.print("No Messages");
    lcd.setCursor(0, 1);
    lcd.print("Waiting");
  }
}

void eject(int message_number) {
  Serial.print("[eject] Message: ");
  Serial.println(message_number);

  // ensure servo is active
  ejectServo.attach(SERVO_PIN);

  // OPEN (must stay powered until fully extended)
  ejectServo.write(SERVO_EJECT);
  delay(2000);   // attempt to open for 2 seconds

  // pause at full extension, wait a full 20 seconds for user to put drawer back in and then latch
  // if I had more time, I would've added a button to tell it when the drawer has reached the back
  delay(20000);

  // close
  ejectServo.write(SERVO_HOME);
  delay(1000);    // attempt to close for 1 second

  ejectServo.detach(); // stop running servo
}

void cutReceipt() {
  // Move cutter forward
  Serial.println("[cut] Cutting");
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);
  analogWrite(PWMA, 255);
  delay(400); 
  
  // Stop for a moment
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, LOW);
  delay(50);
  
  // Return cutter
  Serial.println("[cut] Returning");
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);
  analogWrite(PWMA, 255);
  delay(800); // Can overshoot w/o breaking cuz of the spring limiter
  
  // Stop motor
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, LOW);
  analogWrite(PWMA, 0);
  delay(200);
}
