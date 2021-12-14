#include "DHTesp.h"
#include "EspMQTTClient.h"

#define NETZWERKNAME "FRITZ!Box 7530 MI"
#define PASSWORT "3!2Bp57?CrF193"  
#define MQTT_BROKER "raspberrypi.fritz.box"

EspMQTTClient client(
  "FRITZ!Box 7530 MI",
  "3!2Bp57?CrF193",
  "raspberrypi.fritz.box",  // MQTT Broker server ip
  //"MQTTUsername",   // Can be omitted if not needed
  //"MQTTPassword",   // Can be omitted if not needed
  "Bad_Tmperatur_Luftfeuchte"      // Client name that uniquely identify your device
);
DHTesp dht;
int dhtPin = 14;

int lastMillis = millis();

void setup() {
  dht.setup(dhtPin, DHTesp::DHT11);
}


void onConnectionEstablished() {
  delay(100);
}
void loop() 
{
  client.loop();
  if (millis() - lastMillis > 10000 ){
    lastMillis = millis();
    TempAndHumidity lastValues = dht.getTempAndHumidity();
    client.publish("ESP/Bad_Fenster_Reminder/Output/Temperature", String(lastValues.temperature, 1));
    client.publish("ESP/Bad_Fenster_Reminder/Output/Humidity", String(lastValues.humidity, 1));
  }
}
