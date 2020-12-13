#include <LiquidCrystal.h>

const int RS = 12;  // lcd register select
const int EN = 11;  // lcd enable receiving cmd
const int D4 = 5, D5 = 4, D6 = 3, D7 = 2;  // data pins for sending to lcd
LiquidCrystal lcd(RS, EN, D4, D5, D6, D7);


char recvData[5];  // initially hardcoded to receive 'abcd' from python
boolean availData = false;

void setup() {
    lcd.begin(16,2);     // (col, rows) of lcd
    lcd.print("LCD ready...");
    delay(300);
    Serial.begin(9600);  // baud rate
}

void loop() {
    getData();
    printToLCD();
}

void getData() {
    // Get the number of bytes (characters) available for reading from the serial port. 
    // This is data that’s already arrived and stored in the serial receive buffer (which holds 64 bytes).  

    int bytesAvail = Serial.available(); 

    int idx = 0;
    while (bytesAvail > 0 && availData == false) {
        recvData[idx] = Serial.read();

        delay(300);  // ms
        lcd.setCursor(idx,2);
        lcd.print(recvData[idx]);
        idx++;

        bytesAvail = Serial.available(); 

        // display remaining bytes for debugging
        delay(300);
        lcd.setCursor(13,2);
        lcd.print(bytesAvail);
        if (bytesAvail == 0) {availData = true;}
    }
    recvData[4] = '\0';

}

void printToLCD() {
    if (availData == false) {
        lcd.setCursor(0,1);
        lcd.print("waiting.. ");
        delay(500);
    } 

    if (availData == true) {
        lcd.setCursor(0,1);
        lcd.print("final: ");
        lcd.setCursor(7,1);
        lcd.print(recvData);
        delay(500);
    } 
}
