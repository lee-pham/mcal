#include <WiFi.h>
#include <HTTPClient.h>

const char *ssid = "";                        // Your Wi-Fi network name
const char *password = "";                     // Your Wi-Fi password
const char *serverName = "http://framework.local:5000/data";  // Python server IP

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  unsigned long startMillis = millis();
  while (WiFi.status() != WL_CONNECTED) {
    unsigned long currentMillis = millis();
    if (currentMillis - startMillis > 10000) {  // 10 seconds timeout for Wi-Fi connection
      Serial.println("WiFi connection timed out.");
      return;  // Exit if Wi-Fi fails to connect
    }
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");

  // Proceed with HTTP request only if Wi-Fi is connected
}

void makeHttpRequest() {
  HTTPClient http;
  http.begin(serverName);  // Initialize HTTPClient with server URL

  int httpCode = http.GET();  // Make the HTTP GET request
  Serial.print("HTTP response code: ");
  Serial.println(httpCode);  // Print the HTTP response code

  if (httpCode == 200) {  // HTTP OK
    Serial.println("HTTP request successful.");

    // Check if there's any data in the response stream
    WiFiClient *client = http.getStreamPtr();

    unsigned long startStreamMillis = millis();
    bool dataAvailable = false;

    // Add a small delay to ensure the stream is ready
    delay(100);  // Wait for 100 ms before reading the stream

    // Read the response byte by byte
    while (client->available()) {
      byte b = client->read();
      Serial.print("Received byte: 0x");
      Serial.println(b, HEX);  // Print byte in hex format
      dataAvailable = true;
    }

    // Check if we got any data at all
    if (!dataAvailable) {
      Serial.println("No data received from the server.");
    } else {
      Serial.println("Stream read complete.");
      Serial.println(http.getSize());
    }
  } else {
    Serial.println("HTTP request failed.");
  }

  http.end();  // Close the HTTP connection
}

void loop() {
  makeHttpRequest();
  delay(5000);
}
