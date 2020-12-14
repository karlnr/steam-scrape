#include <LiquidCrystal.h>

const int RS = 12;  // lcd register select
const int EN = 11;  // lcd enable receiving cmd

// map LCD data pins D4-D7 (char display) to arduino digital pins 2-5
const int D4 = 5, D5 = 4, D6 = 3, D7 = 2;
LiquidCrystal lcd(RS, EN, D4, D5, D6, D7);

const int BUFFSIZE = 64;
char recvData[BUFFSIZE];
boolean newData = false;
int bytesAvail = 0;
int bytesRecv = 0;

void setup() {
    lcd.begin(16,2);  // (col, rows) of lcd
    lcd.print("LCD ready.");
    lcd.setCursor(0,1);
    lcd.print("waiting...");
    delay(10);
    Serial.begin(9600);  // baud rate
}

void loop() {
    // getData();  
    // - rename as serialEvent()
    // - automatically called at the end of loop() when there is serial data available in the buffer
    // - https://www.arduino.cc/en/Tutorial/BuiltInExamples/SerialEvent/

    if (newData) {
        printToLCD();
    }
}

void serialEvent() {

    lcd.clear();
    lcd.print("serialEvent...");
    delay(150);
    
    bytesAvail = Serial.available();
    
    int idx = 0;
    bytesRecv = 0;
    while (bytesAvail > 0) {

        lcd.clear();
        lcd.setCursor(0,0);
        lcd.print("bytes avail: ");
        lcd.print(bytesAvail);
        delay(150);

        recvData[idx] = Serial.read();
        idx++;
        bytesRecv = idx;
        
        lcd.setCursor(0,1);
        lcd.print("bytes recv: ");
        lcd.print(bytesRecv);
        delay(150);
        
        bytesAvail = Serial.available();

        // term the string
        if (bytesAvail == 0) {
            recvData[idx] = '\0';
            newData = true;
        }
    }

}

void printToLCD() {
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("msg received: ");
    lcd.setCursor(16,1);  // 16 for autoscroll
    delay(150);

    lcd.autoscroll();
    size_t len = strlen(recvData);
    for (int i = 0; i < strlen(recvData); i++) {
        lcd.print(recvData[i]);
        delay(150);
    }

    if (len < 16) {
        for (int i = 0; i < (16-len); i++){
            lcd.print(" ");
            delay(200);
        }
    }    
    
    sendBytesRecvd();
        newData = false;
}


void sendBytesRecvd() {
    lcd.noAutoscroll();
    delay(500);
    int bytesSent = Serial.println(bytesRecv);
    lcd.clear();
    lcd.print("sent: ");
    lcd.print(bytesSent);
    delay(500);
}
