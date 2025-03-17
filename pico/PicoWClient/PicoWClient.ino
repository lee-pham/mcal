#include <WiFi.h>
// Screen
#include "PDLS_EXT3_Basic_Global.h"
#include "hV_HAL_Peripherals.h"
#include "hV_Configuration.h"

const char* ssid = "";
const char* password = "";

const char* host = "192.168.4.143";
const int port = 5000;

// Define variables and constants
const pins_t boardRaspberryPiPicoW_RP2040 = {
  .panelBusy = 9,               // EXT3 and EXT3.1 pin 3 Red -> GP13
  .panelDC = 8,                 // EXT3 and EXT3.1 pin 4 Orange -> GP12
  .panelReset = 7,              // EXT3 and EXT3.1 pin 5 Yellow -> GP11
  .flashCS = 6,                 // EXT3 and EXT3.1 pin 8 Violet -> GP10
                                //
  .panelCS = 13,                // EXT3 and EXT3.1 pin 9 Grey -> GP17
  .panelCSS = 20,               // EXT3 and EXT3.1 pin 12 Grey2 -> GP14
  .flashCSS = 21,               // EXT3 pin 20 or EXT3.1 pin 11 Black2 -> GP15
                                //
  .touchInt = NOT_CONNECTED,    // EXT3-Touch pin 3 Red -> GP2
  .touchReset = NOT_CONNECTED,  // EXT3-Touch pin 4 Orange -> GP3
  .panelPower = NOT_CONNECTED,  // Optional power circuit
  .cardCS = NOT_CONNECTED,      // Separate SD-card board
  .cardDetect = NOT_CONNECTED,  // Separate SD-card board
};

Screen_EPD_EXT3 myScreen(eScreen_EPD_B98_FS_08, boardRaspberryPiPicoW_RP2040);

WiFiClient client;

const int totalDataSize = 960 * 768 / 8;
int bytesRead = 0;

int initialFreeHeap = rp2040.getFreeHeap();

void setup() {
  Serial.begin(115200);

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

  myScreen.begin();
  myScreen.clear();
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
        byte receivedByte = client.read();
        for (int b = 0; b < 8; b++) {
          if (bitRead(receivedByte, 7 - b) == 1) {
            myScreen.point(x + b, y, myColours.red);
          } else {
            myScreen.point(x + b, y, myColours.white);
          }
        }
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
        }
      }
    }
  }
  Serial.println("Drawing screen");
  myScreen.flush();
  Serial.println("Draw complete");
  delay(10000);
}
