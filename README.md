Sensor Monitoring and Control System
Project Overview
This repository contains the design, implementation, and code for an advanced cloud-based sensor monitoring and control system. Developed as a final project for a B.Sc. in Electrical and Electronics Engineering, this system leverages Arduino Uno and Raspberry Pi to collect real-time environmental data from various sensors and upload it to a cloud platform (ThingsBoard) for remote monitoring, analysis, and automated alerts.

The project addresses the growing demand for smart control and monitoring systems in a connected world, offering an efficient, economical, and modern solution for various applications such as smart agriculture (greenhouses), industrial monitoring, and home automation.

Key Features
Multi-Sensor Integration: Monitors various environmental parameters including:
Light Intensity: Using an LDR sensor.
Humidity: Using a DHT11 sensor.
Temperature: Using a DHT11 sensor.
Distance: Using an HC-SR04 ultrasonic sensor.
Water Level: Using a water level detection sensor.
Real-time Data Acquisition: Collects sensor data continuously via Arduino Uno.
Cloud Connectivity (IoT): Transmits real-time sensor data from Raspberry Pi to a ThingsBoard cloud platform for remote access and visualization.
Local Alerts: Provides audible (buzzer) and visual (LEDs) alerts based on predefined thresholds for sensor readings (e.g., too dark, water not detected, distance too close, humidity/temperature out of range).
Scalable Architecture: Designed with a modular approach, allowing for easy expansion and adaptation to changing requirements.
Cost-Effective Solution: Utilizes affordable yet powerful microcontrollers (Arduino Uno, Raspberry Pi).
Technical Specifications
Hardware Implementation
The system's hardware architecture is designed for robust data acquisition and processing.

Microcontrollers:
Arduino Uno: Serves as the primary interface for collecting data from various analog and digital sensors. It handles initial data processing and communicates with the Raspberry Pi.
Raspberry Pi 4 Model B: Acts as the central processing unit and gateway for cloud communication. It receives data from the Arduino via serial communication and uploads it to ThingsBoard.
Sensors:
Light Sensor (LDR module): Connected to Arduino Analog Pin A0.
Water Level Sensor: Connected to Arduino Analog Pin A5.
Ultrasonic Distance Sensor (HC-SR04): Connected to Arduino Digital Pins 3 (Trig) and 4 (Echo).
DHT11 Temperature and Humidity Sensor: Connected to Arduino Digital Pin 6.
Output Components:
Buzzer: Connected to Arduino Digital Pin 12 for audible alerts.
LEDs: Connected to Arduino Digital Pins 7, 8, 9, 10, 11 for visual alerts corresponding to different sensor conditions.
Connectivity:
USB cable for serial communication between Arduino Uno and Raspberry Pi.
Wi-Fi module (built-in to Raspberry Pi) for internet connectivity.
Power Supply: Standard power supplies for Arduino and Raspberry Pi.
Breadboard: Used for prototyping and connecting components.
Software Implementation
The system's software comprises two main components: Arduino firmware (C++) and Raspberry Pi script (Python).

Arduino Firmware (C++):
Manages sensor readings (analog and digital).
Processes raw sensor data.
Controls local alerts (buzzer, LEDs) based on hardcoded thresholds.
Sends formatted sensor data (distance, humidity, temperature, light, water level) to the Raspberry Pi via serial communication, using 'x' as a delimiter.
Utilizes the DHT.h library for the DHT11 sensor.
Raspberry Pi Script (Python 3):
Serial Communication: Reads incoming sensor data from the Arduino via the /dev/ttyACM0 serial port at 9600 baud.
Data Parsing: Parses the incoming string data, splitting it by 'x' and converting values to floats.
ThingsBoard API Integration: Constructs a JSON payload with sensor data and a timestamp.
Cloud Upload: Sends the JSON payload to the specified ThingsBoard telemetry API endpoint using requests.post().
Error Handling: Includes try-except blocks for robust serial data reading and KeyboardInterrupt handling to gracefully close the serial connection.
Project Structure
Sensor_Monitoring_Control_System/
├── doc/
│   └── Final_Project_Report.pdf   # Full project report (in Hebrew)
├── hardware/
│   ├── schematics/
│   │   ├── arduino_uno_schematic.png # Arduino Uno pinout diagram (Figure 4)
│   │   └── system_circuit_diagram.png # Overall system circuit diagram (Figure 1)
│   ├── images/
│   │   ├── arduino_board.png        # Image of Arduino board (Figure 3)
│   │   ├── water_level_sensor.png   # Image of Water Level Sensor (Figure 5)
│   │   ├── light_sensor.png         # Image of Light Sensor (Figure 6)
│   │   ├── ultrasonic_sensor.png    # Image of Ultrasonic Sensor (Figure 7)
│   │   └── dht11_sensor.png         # Image of DHT11 Sensor (Figure 8)
│   └── components_list.md           # Markdown file with component list and description
├── software/
│   ├── arduino_firmware/
│   │   └── sensor_monitoring.ino    # Arduino C++ code
│   └── raspberry_pi_script/
│       └── thingsboard_uploader.py  # Python script for Raspberry Pi
├── simulation_and_testing/
│   ├── breadboard_setup.jpg         # Photo of the physical breadboard setup (Figure 2)
│   ├── sensor_test_distance.jpg     # Photo of distance sensor test (Figure 9)
│   ├── sensor_test_water_full.jpg   # Photo of water level sensor test (water present) (Figure 10)
│   ├── sensor_test_water_empty.jpg  # Photo of water level sensor test (no water) (Figure 11)
│   ├── sensor_test_temp_humidity.jpg # Photo of temperature/humidity sensor test (Figure 12)
│   └── thingsboard_data_tables/     # Screenshots of ThingsBoard data tables
│       ├── overall_data.png         # Table 2
│       ├── distance_data.png        # Table 3
│       ├── water_full_data.png      # Table 4
│       ├── water_empty_data.png     # Table 5
│       ├── light_dim_data.png       # Table 6
│       ├── light_bright_data.png    # Table 7
│       └── temp_humidity_data.png   # Table 8
├── README.md                      # This file
└── LICENSE                        # Project license (e.g., MIT License)
Setup and Usage
Prerequisites
Hardware:
Arduino Uno board
Raspberry Pi 4 Model B (or compatible)
Water Level Sensor, LDR Light Sensor, HC-SR04 Ultrasonic Sensor, DHT11 Temperature & Humidity Sensor
Buzzer, LEDs, Resistors, Breadboard, Jumper Wires
USB cable (Type A to B for Arduino)
Power supplies for Arduino and Raspberry Pi
Software:
Arduino IDE installed on your computer.
Python 3 installed on your Raspberry Pi.
pyserial and requests Python libraries installed on Raspberry Pi (pip install pyserial requests).
ThingsBoard account and a device created to obtain the thingsboard_url (access token).
