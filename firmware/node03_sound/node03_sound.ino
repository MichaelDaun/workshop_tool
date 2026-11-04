// node-03, Sound waves. A speaker, a microphone and a bar of eight LEDs.
// Arduino-Pico (earlephilhower). Core 1 synthesises the sound, core 0 handles the network.
// Libraries: PubSubClient, ArduinoJson 7, Adafruit NeoPixel.
//
// out/waves  {fa, aa, fb, ab, phase, playing}  two sine waves, Hz, 0-1, degrees
// in/mic     {hz, samples}                     256 samples every 200 ms; the app finds the pitch
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <PWMAudio.h>
#include <Adafruit_NeoPixel.h>
#include "config.h"

const int SPEAKER = 18, MIC = 26, BAR = 22, STATUS = LED_BUILTIN;
const int RATE = 22050, TABLE = 1024, SAMPLES = 256, MIC_HZ = 8000;
const String BASE = String("verkstan/") + ROOM + "/" + NODE + "/";

struct Waves { float fa, aa, fb, ab, phase; bool playing; };
volatile Waves w = { 220, 0.7, 330, 0, 0, false };
volatile float peak = 0;

int16_t sine[TABLE];
PWMAudio out(SPEAKER);
Adafruit_NeoPixel bar(8, BAR, NEO_GRB + NEO_KHZ800);
WiFiClient wifi;
PubSubClient mqtt(wifi);
unsigned long findUntil = 0, lastMic = 0;

// ---- core 1: sound ----

void setup1() {
  for (int i = 0; i < TABLE; i++) sine[i] = 32767 * sin(2 * PI * i / TABLE);
  out.setBuffers(4, 64);
  out.begin(RATE);
}

void loop1() {
  static uint32_t pa = 0, pb = 0;
  static float highest = 0;
  static int n = 0;
  // the phase is a 32-bit counter; its top 10 bits index the table
  uint32_t da = w.fa * 4294967296.0 / RATE, db = w.fb * 4294967296.0 / RATE;
  uint32_t shift = fmodf(w.phase, 360) / 360.0 * 4294967295.0;
  float a = w.playing ? w.aa : 0, b = w.playing ? w.ab : 0;
  for (int i = 0; i < 64; i++) {
    pa += da; pb += db;
    float s = a * sine[pa >> 22] + b * sine[(pb + shift) >> 22];
    s = constrain(s * 0.5f, -32767.0f, 32767.0f);
    highest = max(highest, fabsf(s) / 32767.0f);
    out.write((int16_t)s);
  }
  if (++n >= 40) { peak = highest; highest = 0; n = 0; }
}

// ---- core 0: network ----

void receive(char *topic, byte *data, unsigned int len) {
  String key = String(topic).substring(BASE.length());
  if (key == "out/find") { findUntil = millis() + 3000; return; }
  if (key != "out/waves") return;
  JsonDocument d;
  if (deserializeJson(d, data, len)) return;
  if (!d["fa"].isNull()) w.fa = d["fa"].as<float>();
  if (!d["aa"].isNull()) w.aa = d["aa"].as<float>();
  if (!d["fb"].isNull()) w.fb = d["fb"].as<float>();
  if (!d["ab"].isNull()) w.ab = d["ab"].as<float>();
  if (!d["phase"].isNull()) w.phase = d["phase"].as<float>();
  if (!d["playing"].isNull()) w.playing = d["playing"].as<bool>();
}

void connect() {
  while (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    for (int i = 0; i < 40 && WiFi.status() != WL_CONNECTED; i++) {
      digitalWrite(STATUS, i % 2); delay(250);
    }
  }
  String client = String(NODE) + "-" + String(rp2040.getChipID()).substring(0, 6);
  while (!mqtt.connect(client.c_str(), (BASE + "status").c_str(), 0, true, "gone")) delay(2000);
  mqtt.publish((BASE + "status").c_str(), "up", true);
  mqtt.publish((BASE + "hello").c_str(), "{\"parts\":[\"speaker\",\"mic\",\"bar\"],\"fw\":\"0.3\"}", true);
  mqtt.subscribe((BASE + "out/#").c_str());
}

void sendMic() {
  // 256 samples at 8 kHz take 32 ms
  JsonDocument d;
  d["hz"] = MIC_HZ;
  JsonArray samples = d["samples"].to<JsonArray>();
  unsigned long t = micros();
  for (int i = 0; i < SAMPLES; i++) {
    while (micros() - t < 1000000UL / MIC_HZ) {}
    t += 1000000UL / MIC_HZ;
    samples.add(analogRead(MIC) - 2048);
  }
  char buf[2000];
  size_t n = serializeJson(d, buf, sizeof(buf));
  mqtt.publish((BASE + "in/mic").c_str(), (uint8_t *)buf, n, false);
}

void paintBar() {
  int lit = round(peak * 8);
  for (int i = 0; i < 8; i++) bar.setPixelColor(i, i < lit ? bar.Color(70, 40, 160) : 0);
  bar.show();
}

void setup() {
  pinMode(STATUS, OUTPUT);
  analogReadResolution(12);
  bar.begin();
  bar.setBrightness(40);
  mqtt.setServer(SERVER, 1883);
  mqtt.setCallback(receive);
  mqtt.setBufferSize(2200);
  mqtt.setKeepAlive(30);
}

void loop() {
  if (!mqtt.connected()) connect();
  mqtt.loop();
  if (millis() - lastMic > 200) { lastMic = millis(); sendMic(); }
  paintBar();
  digitalWrite(STATUS, millis() < findUntil ? (millis() / 250) % 2 : 1);
  delay(10);
}
