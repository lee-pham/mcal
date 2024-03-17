#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <LEAmDNS.h>

#ifndef STASSID
#define STASSID "name"
#define STAPSK "pass"
#endif


const char *ssid = STASSID;
const char *password = STAPSK;

WebServer server(80);

const int led = LED_BUILTIN;
#include <EPD_Driver.h>

void handleUpload() {
  Serial.println("Header values");
  Serial.println("User-Agent: " + server.header("User-Agent"));
  Serial.println("Content-Type: " + server.header("Content-Type"));
  String contentLength = server.header("Content-Length");
  Serial.println("Content-Length: " + contentLength);
  Serial.println();

  int numArgs = server.args();
  Serial.println("Num of args: " + String(numArgs));
  for (int i = 0; i <= numArgs; i++) {
    Serial.println(server.argName(i));    
  }

  String body = server.arg("plain");
  int frame[46080];
  for (int i = 0; i <= contentLength.toInt(); i += 2) {
    int pixels = strtol(body.substring(i, i + 2).c_str(), NULL, 16);
    frame[i/2] = pixels;
  }

  server.send(200, "text/plain", "200 OK");
  Serial.println();

  // EPD_Driver epdtest(eScreen_EPD_B98, boardRaspberryPiPico_RP2040_EXT3);
  // epdtest.globalUpdate(data, data, data, data);
  // Turn off CoG`
  // epdtest.COG_powerOff();
}
void setup(void) {
  Serial.begin(115200);
  Serial.println();
  pinMode(led, OUTPUT);
  digitalWrite(led, 0);
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
  server.onFileUpload(handleUpload);

  server.collectHeaders("User-Agent", "Content-Type", "Content-Length");
  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();
}
