#include <EPD_Driver.h>


uint8_t Primary_b[46080];
uint8_t Primary_r[46080];
uint8_t Secondary_b[46080];
uint8_t Secondary_r[46080];


void setup()
{
    EPD_Driver epdtest(eScreen_EPD_B98, boardRaspberryPiPico_RP2040_EXT3);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  digitalWrite(LED_BUILTIN, HIGH);
  // Initialize CoG
  // epdtest.COG_initial();
  Serial.begin(9600);
    while (!Serial);
    Serial.readBytes(Primary_b, 46080);
    Serial.readBytes(Primary_r, 46080);
    Serial.readBytes(Secondary_b, 46080);
    Serial.readBytes(Secondary_r, 46080);


        epdtest.globalUpdate(Primary_b, Primary_r, Secondary_b, Secondary_r);
    // Turn off CoG`
    epdtest.COG_powerOff();

}

void loop() {

  // if (Serial.available() > 0) {
  //   // int data = Serial.readBytesUntil('\n', buffer, 46080);
  //   // Global Update Call
  //   // epdtest.globalUpdate(buffer, buffer, Slavefm1, Slavefm2);
  //   epdtest.globalUpdate(Slavefm1, Slavefm1, Slavefm1, Slavefm2);
  //   // Turn off CoG
  //   epdtest.COG_powerOff();
  // }
  delay(1000);
}