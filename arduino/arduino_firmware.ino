#include <Wire.h>
#include <DHT.h>
#include <BH1750.h>
#include <ArduinoJson.h>

#define DHTPIN 12           // Pin connected to the DHT22 sensor
#define DHTTYPE DHT22       // DHT sensor type
DHT dht(DHTPIN, DHTTYPE);  // Initialize DHT sensor

BH1750 lightMeter;      // Initialize BH1750 sensor

const int soilMoisturePin = A0;  // Pin connected to the soil moisture sensor
const int dry = 595;
const int wet = 239;

// (device1 (45-55), device2 (55-65), device3 (65-75))
const float minThreshold = 55;
const float maxThreshold = 65;

const int waterPin = 2; 
const int mosfetPin = 3;

float volume = 0;
volatile long pulse = 0;
int count = 0;
const float cv = 0.00698; // callibrated variable

#define device_id "device2" //change for every device (device1, device2, device3)

void setup() {
  Serial.begin(9600);
  pinMode(waterPin, INPUT);
  pinMode(mosfetPin, OUTPUT);
  
  // Initialize sensors
  dht.begin();
  Wire.begin();
  lightMeter.begin();
  attachInterrupt(digitalPinToInterrupt(waterPin), increase, RISING);
}

float read_soil_moisture(){
  float soil = analogRead(soilMoisturePin);
  float soilMoisture = map(soil, wet, dry, 100, 0);
  // Serial.println(soilMoisture);
  return soilMoisture;
}

void increase() {
  pulse++;
}

float waterPlant(){
  while(read_soil_moisture() <= maxThreshold){
    digitalWrite(mosfetPin, HIGH); //turn on pump
    // do nothing here, we just waiting for the soil moisture to go to the max
    delay(1000); // siram 1 detik
    count += 1;
    if(count > 30){ // already 30 sec
      count = 0;
      return -1; //water pump not working
    }
    digitalWrite(mosfetPin, LOW);
    delay(10000);
  }
  digitalWrite(mosfetPin, LOW); //turn off pump
  volume = cv * pulse; //calculate volume of water used
  pulse = 0; //reset the pulse variable
  return volume;
}

void loop() {
  // Read data from sensors
  float temperature = dht.readTemperature(); //read temperature level (DHT22)
  float humidity = dht.readHumidity(); //read humidity level (DHT22)
  float lightIntensity = lightMeter.readLightLevel(); //read light level (BH1750)
  float soilMoisture = read_soil_moisture(); //read soil moisture (HW-390 (Capacitive Soil Moisture Sensor))
  float waterUsage = 0; //variable for water flow sensor. IF waterUsage 0 then plantwatering = False && dont send json data (raspberry pi)

  if(soilMoisture < minThreshold){
    waterUsage = waterPlant(); //water the plant
  }
  
  // turn it into json format
  StaticJsonDocument<200> doc; //json variable. (time will be sent to the database in the rpi)

  doc["id"] = device_id;
  doc["deviceID"] = device_id;
  doc["t"] = temperature;
  doc["h"] = humidity;
  doc["l"] = lightIntensity;
  doc["s"] = soilMoisture;
  doc["w"] = waterUsage;
  
  serializeJson(doc, Serial); //print json in serial
  Serial.println();
  delay(5000);  // delay 5 seconds
}