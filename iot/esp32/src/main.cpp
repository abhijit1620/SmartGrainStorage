#include <Arduino.h>
#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ---- PIN CONFIG ----
#define DHTPIN 4
#define DHTTYPE DHT22
#define MQ135_PIN 34
#define RELAY_PIN 5
#define BUZZER_PIN 18

// ---- OBJECTS ----
DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ---- THRESHOLDS ----
float TEMP_LIMIT = 30.0;
float HUM_LIMIT = 70.0;
int GAS_LIMIT = 450;

// ---- SETUP ----
void setup() {
    Serial.begin(115200);
    
    dht.begin();
    lcd.init();
    lcd.backlight();

    pinMode(RELAY_PIN, OUTPUT);
    pinMode(BUZZER_PIN, OUTPUT);

    digitalWrite(RELAY_PIN, LOW);
    digitalWrite(BUZZER_PIN, LOW);

    lcd.setCursor(0, 0);
    lcd.print("Grain Storage");
    lcd.setCursor(0, 1);
    lcd.print("System Start...");
    delay(2000);
    lcd.clear();
}

// ---- LOOP ----
void loop() {
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();
    int gas = analogRead(MQ135_PIN);

    // Serial Print
    Serial.print("Temp: "); Serial.print(temp);
    Serial.print(" | Hum: "); Serial.print(hum);
    Serial.print(" | Gas: "); Serial.println(gas);

    // LCD Display
    lcd.setCursor(0, 0);
    lcd.print("T:");
    lcd.print(temp);
    lcd.print("C ");

    lcd.setCursor(8, 0);
    lcd.print("H:");
    lcd.print(hum);
    lcd.print("% ");

    lcd.setCursor(0, 1);
    lcd.print("Gas:");
    lcd.print(gas);
    lcd.print("     ");

    // ALERT SYSTEM
    bool danger = false;

    if (temp > TEMP_LIMIT || hum > HUM_LIMIT || gas > GAS_LIMIT) {
        danger = true;
    }

    if (danger) {
        digitalWrite(RELAY_PIN, HIGH); // turn ON fan
        digitalWrite(BUZZER_PIN, HIGH); // buzzer ON
        lcd.setCursor(0, 1);
        lcd.print("!! ALERT ACTIVE !!");
    } else {
        digitalWrite(RELAY_PIN, LOW);
        digitalWrite(BUZZER_PIN, LOW);
    }

    delay(2000);
}