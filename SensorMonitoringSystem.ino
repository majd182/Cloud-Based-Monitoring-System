// Sensor Monitoring System for Arduino

// --- Sensor Pin Definitions ---
int WaterLevel = 0;   // Variable to hold the water level sensor reading
int Waterpin = A5;    // Analog pin for the water level sensor

const int trigPin = 3;  // Digital pin for the ultrasonic sensor (Trig)
const int echoPin = 4;  // Digital pin for the ultrasonic sensor (Echo)
long duration;          // Variable to store ultrasonic pulse duration
int distance;           // Variable to store calculated distance in cm

#include "DHT.h"      // Include the DHT sensor library (for temperature and humidity)
DHT dht;                // Create a DHT object

int buzzer = 12;      // Digital pin for the buzzer

// --- LED Warning Indicators ---
// (Pins 7, 8, 9, 10, 11 are used for various warnings)
// Pin 7: Ultrasonic (distance) warning
// Pin 8: Light sensor (darkness) warning
// Pin 9: Temperature warning
// Pin 10: Humidity warning
// Pin 11: Water level warning

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate

  // Ultrasonic sensor pin modes
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT);  // Sets the echoPin as an Input

  // DHT sensor setup (specify data pin)
  dht.setup(6);             // Set pin 6 for DHT sensor data communication

  // Buzzer and LED pin modes
  pinMode(buzzer, OUTPUT);
  pinMode(7, OUTPUT);   // LED for ultrasonic warning
  pinMode(8, OUTPUT);   // LED for light sensor warning
  pinMode(9, OUTPUT);   // LED for temperature warning
  pinMode(10, OUTPUT);  // LED for humidity warning
  pinMode(11, OUTPUT);  // LED for water level warning
}

void loop() {
  // --- Light Sensor Reading (Analog Pin A0) ---
  int analogValue = analogRead(A0); // Reads the input on analog pin A0 (value between 0 and 1023)
  delay(1000); // Delay to stabilize readings and prevent noise

  // Check light conditions and trigger warning if dark
  if (analogValue < 100) {
    // Serial.println(" - Very bright"); // Uncomment for serial debug
    noTone(buzzer);
    digitalWrite(8, LOW); // Turn off light warning LED
  } else if (analogValue < 200) {
    // Serial.println(" - Bright");
    noTone(buzzer);
    digitalWrite(8, LOW);
  } else if (analogValue < 500) {
    // Serial.println(" - Light");
    noTone(buzzer);
    digitalWrite(8, LOW);
  } else if (analogValue < 800) {
    // Serial.println(" - Dim");
    noTone(buzzer);
    digitalWrite(8, LOW);
  } else {
    // Serial.println(" - Dark");
    tone(buzzer, 2000, 1500); // Play a tone (2000Hz for 1.5s)
    digitalWrite(8, HIGH);    // Turn on light warning LED
  }
  delay(1000); // Short delay after light sensor processing

  // --- Water Level Sensor Reading (Analog Pin A5) ---
  WaterLevel = analogRead(Waterpin); // Read data from analog pin and store it to WaterLevel variable

  // Check water level and trigger warning if detected
  if (WaterLevel < 100) {
    // Serial.println("water not detected"); // Uncomment for serial debug
    noTone(buzzer);
    digitalWrite(11, LOW); // Turn off water level warning LED
  } else {
    // Serial.println("water detected");
    tone(buzzer, 2000, 2000); // Play a tone (2000Hz for 2s)
    digitalWrite(11, HIGH);   // Turn on water level warning LED
  }
  delay(1000); // Short delay after water level sensor processing

  // --- Ultrasonic Sensor Reading (Distance Measurement) ---
  // Clears the trigPin by setting it LOW
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance (speed of sound ~0.034 cm/us)
  distance = duration * 0.034 / 2;

  // Serial.print("Distance: "); // Uncomment for serial debug
  // Serial.print(distance);
  // Serial.println(" cm");

  // Check distance and trigger warning if too close (e.g., < 10cm)
  if (distance < 10) {
    tone(buzzer, 2000, 1500); // Play a tone (2000Hz for 1.5s)
    digitalWrite(7, HIGH);    // Turn on ultrasonic warning LED
  } else {
    noTone(buzzer);
    digitalWrite(7, LOW);     // Turn off ultrasonic warning LED
  }
  delay(1000); // Short delay after ultrasonic sensor processing

  // --- Temperature & Humidity Sensor Reading (DHT) ---
  delay(dht.getMinimumSamplingPeriod()); // Delay for DHT sensor stability
  float humidity = dht.getHumidity();    // Get humidity value
  float temperature = dht.getTemperature(); // Get temperature value

  // Uncomment the following lines for serial debug of DHT readings
  // Serial.println();
  // Serial.println("Status\tHumidity (%)\tTemperature (C)\t(F)");
  // Serial.print(dht.getStatusString());
  // Serial.print("\t");
  // Serial.print(humidity, 1);
  // Serial.print("\t\t");
  // Serial.print(temperature, 1);
  // Serial.print("\t\t");
  // Serial.println(dht.toFahrenheit(temperature), 1);

  // Check humidity and trigger warning if out of range (e.g., <40% or >70%)
  if (humidity > 70 || humidity < 40) {
    tone(buzzer, 2000, 1500); // Play a tone (2000Hz for 1.5s)
    digitalWrite(10, HIGH);   // Turn on humidity warning LED
  } else {
    noTone(buzzer);
    digitalWrite(10, LOW);    // Turn off humidity warning LED
  }

  // Check temperature and trigger warning if out of range (e.g., <10C or >30C)
  if (temperature > 30 || temperature < 10) {
    tone(buzzer, 2000, 1500); // Play a tone (2000Hz for 1.5s)
    digitalWrite(9, HIGH);    // Turn on temperature warning LED
  } else {
    noTone(buzzer);
    digitalWrite(9, LOW);     // Turn off temperature warning LED
  }

  // --- Print all sensor values to Serial Monitor (delimited by 'x') ---
  // This format is useful for sending data to a serial plotter or other applications
  Serial.print(distance);
  Serial.print('x');
  Serial.print(humidity);
  Serial.print('x');
  Serial.print(temperature);
  Serial.print('x');
  Serial.print(analogValue);
  Serial.print('x');
  Serial.println(WaterLevel); // Use println for the last value to ensure a new line

  delay(2000); // Overall delay before the next loop iteration
}
