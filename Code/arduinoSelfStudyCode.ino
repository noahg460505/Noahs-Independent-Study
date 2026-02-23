#include <LiquidCrystal.h>

// Initialize LCD with your specific pins (RS, E, D4, D5, D6, D7)
const int rs = 13, en = 12, d4 = 11, d5 = 10, d6 = 9, d7 = 8;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

String inputBuffer = ""; 

void setup() {
  lcd.begin(16, 2);
  lcd.print("Starting...");
  Serial.begin(9600);
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
  // ejection code, motor ejects message from slot in box
}

void display(int msg_id, int remaining_seconds) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Msg #");
  lcd.print(msg_id);
  lcd.setCursor(0, 1);
  lcd.print(remaining_seconds);
}