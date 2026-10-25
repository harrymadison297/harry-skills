#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define DHT_PIN 4
#define LED_PIN 2

const char* WIFI_SSID = "home";
const char* WIFI_PASS = "secret";
const char* MQTT_HOST = "192.168.1.10";

DHT dht(DHT_PIN, DHT22);
WiFiClient wifi;
PubSubClient mqtt(wifi);

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  dht.begin();
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  mqtt.setServer(MQTT_HOST, 1883);
}

void loop() {
  if (!mqtt.connected()) {
    mqtt.connect("kitchen-node");
  }
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  char payload[64];
  snprintf(payload, sizeof(payload), "{\"t\":%.1f,\"h\":%.1f}", t, h);
  mqtt.publish("home/kitchen/climate", payload);
  digitalWrite(LED_PIN, HIGH);
  delay(100);
  digitalWrite(LED_PIN, LOW);
  delay(10000);
}
