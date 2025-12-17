#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

// ================= LCD =================
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ================= DHT =================
#define DHTPIN 4
#define DHTTYPE DHT22        // 🔥 DHT11 hai to DHT11
DHT dht(DHTPIN, DHTTYPE);

// ================= MQ135 =================
#define MQ135_PIN 34

// ================= WIFI =================
const char* ssid = "11012007";
const char* password = "12345678";

// ================= FLASK =================
String serverURL = "http://10.84.58.43:5050/data";

// ================= GPIO =================
#define BUZZER 18
#define RELAY  23   // FAN RELAY

unsigned long lastBeep = 0;

void setup() {
  Serial.begin(115200);

  pinMode(BUZZER, OUTPUT);
  pinMode(RELAY, OUTPUT);
  digitalWrite(BUZZER, LOW);
  digitalWrite(RELAY, LOW);

  // ---------- LCD ----------
  Wire.begin(21, 22);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("Smart Grain");
  lcd.setCursor(0,1);
  lcd.print("Booting...");
  delay(1500);

  // ---------- DHT ----------
  dht.begin();

  // ---------- WIFI ----------
  WiFi.begin(ssid, password);
  lcd.clear();
  lcd.print("Connecting WiFi");

  int tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries < 20) {
    delay(500);
    tries++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    lcd.clear();
    lcd.print("WiFi Connected");
    Serial.println(WiFi.localIP());
  } else {
    lcd.clear();
    lcd.print("WiFi FAILED");
    while (1);
  }

  delay(1500);
}

void loop() {

  // ========== SENSOR READ ==========
  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  // Safety fallback
  if (isnan(temp) || isnan(hum)) {
    temp = 28.0;
    hum  = 55.0;
  }

  int mqRaw = analogRead(MQ135_PIN);
  float co2 = map(mqRaw, 0, 4095, 400, 2000);
  float ammonia = map(mqRaw, 0, 4095, 0, 100) / 10.0;

  String status = "Safe";
  float confidence = 0.4;

  unsigned long now = millis();

  // ========== FAN + BUZZER LOGIC ==========
  if (hum > 70) {
    // -------- SPOILAGE --------
    status = "Spoilage";
    confidence = 0.95;

    digitalWrite(RELAY, HIGH);     // FAN ON
    digitalWrite(BUZZER, HIGH);    // BUZZER CONTINUOUS
  }
  else if (hum > 60) {
    // -------- RISK --------
    status = "Risk";
    confidence = 0.75;

    digitalWrite(RELAY, HIGH);     // FAN ON

    // Mild intermittent buzzer
    if (now - lastBeep >= 1200) {
      lastBeep = now;
      digitalWrite(BUZZER, HIGH);
    }
    if (now - lastBeep >= 300) {
      digitalWrite(BUZZER, LOW);
    }
  }
  else {
    // -------- SAFE --------
    digitalWrite(RELAY, LOW);      // FAN OFF
    digitalWrite(BUZZER, LOW);     // BUZZER OFF
  }

  // ========== LCD ==========
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("T:");
  lcd.print(temp,1);
  lcd.print(" H:");
  lcd.print(hum,0);

  lcd.setCursor(0,1);
  lcd.print(status);

  // ========== SEND TO FLASK ==========
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{"
      "\"temp\":" + String(temp,1) + ","
      "\"hum\":" + String(hum,1) + ","
      "\"co2\":" + String(co2) + ","
      "\"ammonia\":" + String(ammonia,2) + ","
      "\"status\":\"" + status + "\","
      "\"confidence\":" + String(confidence) +
    "}";

    http.POST(jsonData);
    http.end();
  }

  delay(4000);
}