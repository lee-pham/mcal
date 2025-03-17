// Screen
#include "PDLS_EXT3_Basic_Global.h"

// SDK
// #include <Arduino.h>
#include "hV_HAL_Peripherals.h"

// Include application, user and local libraries
// #include <SPI.h>

// Configuration
#include "hV_Configuration.h"

// Set parameters

// Define variables and constants
const pins_t boardRaspberryPiPicoW_RP2040 = {
  .panelBusy = 9,               ///< EXT3 and EXT3.1 pin 3 Red -> GP13
  .panelDC = 8,                 ///< EXT3 and EXT3.1 pin 4 Orange -> GP12
  .panelReset = 7,              ///< EXT3 and EXT3.1 pin 5 Yellow -> GP11
  .flashCS = 6,                 ///< EXT3 and EXT3.1 pin 8 Violet -> GP10
                                //
  .panelCS = 13,                ///< EXT3 and EXT3.1 pin 9 Grey -> GP17
  .panelCSS = 20,               ///< EXT3 and EXT3.1 pin 12 Grey2 -> GP14
  .flashCSS = 21,               ///< EXT3 pin 20 or EXT3.1 pin 11 Black2 -> GP15
  .touchInt = NOT_CONNECTED,    ///< EXT3-Touch pin 3 Red -> GP2
  .touchReset = NOT_CONNECTED,  ///< EXT3-Touch pin 4 Orange -> GP3
  .panelPower = NOT_CONNECTED,  ///< Optional power circuit
  .cardCS = NOT_CONNECTED,      ///< Separate SD-card board
  .cardDetect = NOT_CONNECTED,  ///< Separate SD-card board
};

Screen_EPD_EXT3 myScreen(eScreen_EPD_B98_FS_08, boardRaspberryPiPicoW_RP2040);


#include <WiFi.h>

// Replace with your network credentials
const char* ssid = "";
const char* password = "";

// Server details
const char* host = "192.168.4.143";
const int port = 5000;

WiFiClient client;

const int totalDataSize = 960 * 768 / 8;
int bytesRead = 0;

int initialFreeHeap = rp2040.getFreeHeap();

void setup() {
  Serial.begin(115200);
  myScreen.begin();
  myScreen.clear();

  Serial.println("Connecting to WiFi");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  if (client.connect(host, port)) {
    Serial.println("Connected to server");
  } else {
    Serial.println("Connection failed. Rebooting.");
    rp2040.reboot();
  }
}

void loop() {
  int x = 0;
  int y = 0;
  Serial.println("Requesting transfer");
  client.print("Ready to receive");
  bool transferIncomplete = true;
  while (transferIncomplete) {
    if (client.available()) {
      Serial.println("Transfer in progress");
      String progress = "";
      while (client.available()) {
        byte receivedByte = client.read();  // Read a single byte
        for (int b = 0; b < 8; b++) {
          if (bitRead(receivedByte, 7 - b) == 1) {
            myScreen.point(x + b, y, myColours.red);
          } else {
            myScreen.point(x + b, y, myColours.white);
          }
        }

        // if (receivedByte == '1') {
        //   myScreen.point(x, y, myColours.red);
        //   myScreen.point(x + 1, y, myColours.red);
        //   myScreen.point(x + 2, y, myColours.red);
        //   myScreen.point(x + 3, y, myColours.red);
        //   myScreen.point(x + 4, y, myColours.red);
        //   myScreen.point(x + 5, y, myColours.red);
        //   myScreen.point(x + 6, y, myColours.red);
        //   myScreen.point(x + 7, y, myColours.red);

        // } else {
        //   myScreen.point(x, y, myColours.white);
        //   myScreen.point(x + 1, y, myColours.white);
        //   myScreen.point(x + 2, y, myColours.white);
        //   myScreen.point(x + 3, y, myColours.white);
        //   myScreen.point(x + 4, y, myColours.white);
        //   myScreen.point(x + 5, y, myColours.white);
        //   myScreen.point(x + 6, y, myColours.white);
        //   myScreen.point(x + 7, y, myColours.white);
        // }
        x += 8;
        if (x >= myScreen.screenSizeX()) {
          x = 0;
          y += 1;
        }
        if (x == myScreen.screenSizeX() && y == myScreen.screenSizeY()) {
          x = 0;
          y = 0;
        }
        bytesRead++;
        if (bytesRead % 1840 == 0) {
          progress += "#";
          Serial.print("[" + progress);
          String spaces = "";
          for (int i = 0; i < 50 - progress.length(); i++) {
            spaces += " ";
          }
          Serial.print(spaces);
          Serial.println("]\t" + String(bytesRead) + "\t/\t" + String(totalDataSize));
        } else if (bytesRead == totalDataSize) {
          Serial.print("[##################################################]\t");
          Serial.println(String(bytesRead) + "\t/\t" + String(totalDataSize) + "\tTransfer complete!");
          transferIncomplete = false;
          bytesRead = 0;
          // Serial.println(String(initialFreeHeap) + " " + String(rp2040.getFreeHeap()));
          Serial.print(bitRead(receivedByte, 7));
          Serial.print(bitRead(receivedByte, 6));
          Serial.print(bitRead(receivedByte, 5));
          Serial.print(bitRead(receivedByte, 4));
          Serial.print(bitRead(receivedByte, 3));
          Serial.print(bitRead(receivedByte, 2));
          Serial.print(bitRead(receivedByte, 1));
          Serial.println(bitRead(receivedByte, 0));
        }
      }
    }
  }
  Serial.println("Drawing screen");
  myScreen.flush();
  Serial.println("Draw complete");
  delay(10000);
}
