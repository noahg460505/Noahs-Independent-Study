#include <LiquidCrystal.h>

// Initialize LCD with your specific pins (RS, E, D4, D5, D6, D7)
const int rs = 13, en = 12, d4 = 11, d5 = 10, d6 = 9, d7 = 8;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

//the motor will be controlled by the motor A pins on the motor driver

//driver for the motor A
const int PWMA = 5;           //speed control pin on the motor driver for motor A
const int AIN1 = 7;           //control pin 1 on the motor driver for the motor A
const int AIN2 = 6;           //control pin 2 on the mot
const int BIN1 = 2;           //control pin 1 on the motor driver for the motor B
const int BIN2 = 4;           //control pin 2 on the motor driver for the motor B
const int PWMB = 3;           //speed control pin on the motor driver for motor B


String inputBuffer = ""; 
int motorSpeed = 0; 

void setup() {
  lcd.begin(16, 2);
  lcd.print("Starting...");
  Serial.begin(9600);

  // Set the motor control pins as outputs
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(PWMA, OUTPUT);

  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  pinMode(PWMB, OUTPUT);
  
  // Initialize motors to be stopped
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, LOW);
  analogWrite(PWMA, 0);

  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, LOW);
  analogWrite(PWMB, 0);
}

void loop() {
  // wacky non-blocking code i found for recieving serial
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

  // eject the requested message specificied after [eject] command
  if (command.startsWith("[eject]")) { 
    if (firstSpace != -1) {
      int message_number = command.substring(firstSpace + 1).toInt();
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
  // show ejection message
  else if (command.startsWith("[ejecting]")) {
    if (firstSpace != -1) {
      int message_number = command.substring(firstSpace + 1).toInt();
      display("ejecting", message_number, 0);
      eject(message_number);
    }
  }
  // show no messages
  else if (command.startsWith("[no_messages]")) {
    display("no_messages", 0, 0);
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
  Serial.print("[eject] Ejected message: ");
  Serial.println(message_number);
  
  if (message_number < 1) {
    // Run motor A forward for 2 seconds
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    analogWrite(PWMA, 200);
    delay(2000);
    // Stop motor A
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, LOW);
    analogWrite(PWMA, 0);
  }
  if (message_number >= 1) {
    // Run motor A forward for 2 seconds
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
    analogWrite(PWMB, 200);
    delay(2000);
    // Stop motor B
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, LOW);
    analogWrite(PWMB, 0);
  }
}
