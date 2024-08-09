#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

#ifndef STASSID
#define STASSID ""
#define STAPSK ""
#endif

const char *ssid = STASSID;
const char *pass = STAPSK;

WiFiMulti WiFiMulti;

void setup() {

  Serial.begin(115200);

  Serial.println();
  Serial.println();
  Serial.println();

  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }

  WiFiMulti.addAP(ssid, pass);
}

void loop() {
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    if (http.begin("http://192.168.1.65:5000")) {  // HTTP


      Serial.print("[HTTP] GET...\n");
      // start connection and send HTTP header
      int httpCode = http.GET();

      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] GET... code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          int length = http.getSize();
          uint8_t *buffer = new uint8_t[length];
          WiFiClient &stream = http.getStream();
          int bytesRead = 0;
          while (http.connected() && (bytesRead < length)) {
            size_t size = stream.available();
            if (size) {
              int c = stream.readBytes(buffer + bytesRead, size);
              bytesRead += c;
            }
          }
          Serial.print("Payload as byte array: ");
          for (int i = 0; i < length; i++) {
            Serial.printf("%02x ", buffer[i]);
          }
          Serial.println();
          Serial.println(buffer[length - 1]);
          delete[] buffer;
        }
      } else {
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
      }

      http.end();
    } else {
      Serial.printf("[HTTP} Unable to connect\n");
    }
  }
  delay(5000);
}
