#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <LEAmDNS.h>

#ifndef STASSID
#define STASSID "ssid"
#define STAPSK "passw"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

WebServer server(80);

const int led = LED_BUILTIN;


void handleUpload() {
  digitalWrite(led, 0);
  Serial.println(server.upload().filename);
  Serial.println(server.upload().totalSize);
  // Serial.write(server.upload().buf, server.upload().totalSize);
  server.send(200, "text/plain", "thanks for the upload!\r\n");
  digitalWrite(led, 1);
}

void setup(void) {
  pinMode(led, OUTPUT);
  digitalWrite(led, 0);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(led, 1);
    delay(250);
    digitalWrite(led, 0);
    delay(250);
    Serial.print(".");
  }
  digitalWrite(led, 1);
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("picow")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleUpload);
  
  // server.onFileUpload(handleUpload);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();
}
