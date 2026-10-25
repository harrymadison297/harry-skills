#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

DHT dht(4, DHT22);
WiFiClient wifi;
PubSubClient mqtt(wifi);

void setup() {
  dht.begin();
  WiFi.begin("home", "secret");
  while (WiFi.status() != WL_CONNECTED) delay(500);
  mqtt.setServer("192.168.1.10", 1883);
}

void loop() {
  if (!mqtt.connected()) mqtt.connect("kitchen-node");
  char payload[64];
  snprintf(payload, sizeof(payload), "{\"t\":%.1f,\"h\":%.1f}", dht.readTemperature(), dht.readHumidity());
  mqtt.publish("home/kitchen/climate", payload);
  delay(10000);
}
