// Ljudvågor (nod-03): högtalare, mikrofon och en stapel med åtta lysdioder.
// Arduino-Pico (earlephilhower). Kärna 1 räknar fram ljudet, kärna 0 sköter nätet.
// Bibliotek: PubSubClient, ArduinoJson 7, Adafruit NeoPixel.
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <PWMAudio.h>
#include <Adafruit_NeoPixel.h>
#include "config.h"

const int LJUD = 18, MIK = 26, STAPEL = 22, STATUS = LED_BUILTIN;
const int TAKT = 22050, TABELL = 1024, PROV = 256, MIK_HZ = 8000;
const String BAS = String("verkstan/") + RUM + "/" + NOD + "/";

struct Vagor { float fa, aa, fb, ab, fas; bool spelar; };
volatile Vagor v = { 220, 0.7, 330, 0, 0, false };
volatile float topp = 0;

int16_t sinus[TABELL];
PWMAudio ut(LJUD);
Adafruit_NeoPixel stapel(8, STAPEL, NEO_GRB + NEO_KHZ800);
WiFiClient wifi;
PubSubClient mqtt(wifi);
unsigned long hittaTill = 0, senastMik = 0;

// ---- kärna 1: ljudet ----

void setup1() {
  for (int i = 0; i < TABELL; i++) sinus[i] = 32767 * sin(2 * PI * i / TABELL);
  ut.setBuffers(4, 64);
  ut.begin(TAKT);
}

void loop1() {
  static uint32_t pa = 0, pb = 0;
  static float hogst = 0;
  static int n = 0;
  // fasen räknas i 32 bitar, de översta 10 bitarna pekar i tabellen
  uint32_t da = v.fa * 4294967296.0 / TAKT, db = v.fb * 4294967296.0 / TAKT;
  uint32_t forskjut = fmodf(v.fas, 360) / 360.0 * 4294967295.0;
  float a = v.spelar ? v.aa : 0, b = v.spelar ? v.ab : 0;
  for (int i = 0; i < 64; i++) {
    pa += da; pb += db;
    float s = a * sinus[pa >> 22] + b * sinus[(pb + forskjut) >> 22];
    s = constrain(s * 0.5f, -32767.0f, 32767.0f);
    hogst = max(hogst, fabsf(s) / 32767.0f);
    ut.write((int16_t)s);
  }
  if (++n >= 40) { topp = hogst; hogst = 0; n = 0; }
}

// ---- kärna 0: nätet ----

void taEmot(char *amne, byte *data, unsigned int len) {
  String sak = String(amne).substring(BAS.length());
  if (sak == "ut/hitta") { hittaTill = millis() + 3000; return; }
  if (sak != "ut/vagor") return;
  JsonDocument d;
  if (deserializeJson(d, data, len)) return;
  if (!d["fa"].isNull()) v.fa = d["fa"].as<float>();
  if (!d["aa"].isNull()) v.aa = d["aa"].as<float>();
  if (!d["fb"].isNull()) v.fb = d["fb"].as<float>();
  if (!d["ab"].isNull()) v.ab = d["ab"].as<float>();
  if (!d["fas"].isNull()) v.fas = d["fas"].as<float>();
  if (!d["spelar"].isNull()) v.spelar = d["spelar"].as<bool>();
}

void anslut() {
  while (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(WIFI_NAMN, WIFI_LOSEN);
    for (int i = 0; i < 40 && WiFi.status() != WL_CONNECTED; i++) {
      digitalWrite(STATUS, i % 2); delay(250);
    }
  }
  String klient = String(NOD) + "-" + String(rp2040.getChipID()).substring(0, 6);
  while (!mqtt.connect(klient.c_str(), (BAS + "status").c_str(), 0, true, "borta")) delay(2000);
  mqtt.publish((BAS + "status").c_str(), "uppe", true);
  mqtt.publish((BAS + "hej").c_str(), "{\"har\":[\"hogtalare\",\"mik\",\"stapel\"],\"fw\":\"0.2\"}", true);
  mqtt.subscribe((BAS + "ut/#").c_str());
}

void skickaMik() {
  // 256 prov i 8 kHz tar 32 ms
  JsonDocument d;
  d["hz"] = MIK_HZ;
  JsonArray prov = d["prov"].to<JsonArray>();
  unsigned long t = micros();
  for (int i = 0; i < PROV; i++) {
    while (micros() - t < 1000000UL / MIK_HZ) {}
    t += 1000000UL / MIK_HZ;
    prov.add(analogRead(MIK) - 2048);
  }
  char buf[2000];
  size_t n = serializeJson(d, buf, sizeof(buf));
  mqtt.publish((BAS + "in/mik").c_str(), (uint8_t *)buf, n, false);
}

void visaStapel() {
  int tanda = round(topp * 8);
  for (int i = 0; i < 8; i++) stapel.setPixelColor(i, i < tanda ? stapel.Color(70, 40, 160) : 0);
  stapel.show();
}

void setup() {
  pinMode(STATUS, OUTPUT);
  analogReadResolution(12);
  stapel.begin();
  stapel.setBrightness(40);
  mqtt.setServer(SERVER, 1883);
  mqtt.setCallback(taEmot);
  mqtt.setBufferSize(2200);
  mqtt.setKeepAlive(30);
}

void loop() {
  if (!mqtt.connected()) anslut();
  mqtt.loop();
  if (millis() - senastMik > 200) { senastMik = millis(); skickaMik(); }
  visaStapel();
  digitalWrite(STATUS, millis() < hittaTill ? (millis() / 250) % 2 : 1);
  delay(10);
}
