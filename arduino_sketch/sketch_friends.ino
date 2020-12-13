#include <LiquidCrystal.h>

const int RS = 12;  // lcd register select
const int EN = 11;  // lcd enable receiving cmd
const int D4 = 5, D5 = 4, D6 = 3, D7 = 2;  // data pins for sending to lcd
LiquidCrystal lcd(RS, EN, D4, D5, D6, D7);

char recvData;
boolean availData = false;

void setup() {
    lcd.begin(16,2);     // (col, rows) of lcd
    lcd.print("LCD ready...");
    Serial.begin(9600);  // baud rate
}

void loop() {
    getData();
    printToLCD();
}

void getData() {
    if (Serial.available() > 0) {
        recvData = Serial.read();
        availData = true;
    }
}

void printToLCD() {
    if (availData == true) {
        lcd.setCursor(0,1);
        lcd.print(recvData);
        availData = false;
    }
}
