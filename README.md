# **Cloud-Based Monitoring and Control System**

## **Overview**
This project demonstrates an IoT-based solution for real-time monitoring and control of environmental parameters. It combines hardware (Arduino Uno, Raspberry Pi, and various sensors) with cloud technologies to provide an intelligent and scalable system for applications such as smart homes, agriculture, and industrial automation.

---

## **Features**
- **Real-time Monitoring:** Collects data on temperature, humidity, water levels, light intensity, and distance using sensors.
- **Remote Control:** Allows users to control connected devices via a cloud-based dashboard (ThingsBoard).
- **Alerts & Automation:** Automatically triggers actions (e.g., notifications, device controls) when thresholds are exceeded.
- **Data Visualization:** Real-time data displayed through dynamic graphs and visual dashboards.
- **Scalable Design:** Easily extendable to additional sensors or use cases.

---

## **Technologies Used**
- **Hardware:**
  - Arduino Uno
  - Raspberry Pi
  - DHT11 (Temperature and Humidity Sensor)
  - Ultrasonic Distance Sensor
  - Light Sensor
  - Water Level Sensor
- **Software:**
  - Python (Data processing and control logic)
  - ThingsBoard (Cloud dashboard and remote control)
  - MQTT and HTTP protocols for communication
- **Cloud Integration:** ThingsBoard for telemetry and device management
- **Other Tools:** RPi.GPIO, Adafruit_DHT libraries for hardware control

---

## **Project Structure**
```plaintext
Cloud-Based-Monitoring-System/
│
├── main.py                 # Main script for system operation
├── sensor_readings.py      # Module to read sensor data
├── mqtt_client.py          # MQTT client for communication
├── data_processing.py      # Data validation and formatting
├── thingsboard_integration.py # ThingsBoard cloud integration
├── automation_rules.py     # Automation and alert logic
├── config.py               # Configuration file
├── test_sensors.py         # Script to test sensor functionality
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

---

## **Setup Instructions**
### **Hardware Setup**
1. Connect the sensors (DHT11, ultrasonic, light, and water level) to the Raspberry Pi and Arduino Uno as per the wiring diagram.
2. Configure GPIO pins for each sensor in `sensor_readings.py`.

### **Software Setup**
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/Cloud-Based-Monitoring-System.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Cloud-Based-Monitoring-System
   ```
3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure MQTT and ThingsBoard credentials in `config.py`.

### **Running the System**
1. Test the sensors:
   ```bash
   python test_sensors.py
   ```
2. Start the system:
   ```bash
   python main.py
   ```

---

## **Usage**
- Monitor sensor data and control devices remotely via the ThingsBoard dashboard.
- Alerts and actions are triggered automatically based on predefined rules in `automation_rules.py`.

---

## **Results**
- Real-time environmental data visualization on the ThingsBoard dashboard.
- Notifications and automation for critical conditions like high temperature or low water levels.
- Modular and extensible system for future enhancements.

---

## **Contributing**
Contributions are welcome! Feel free to open issues or submit pull requests for improvements or new features.

---

## **Contact**
For questions or collaboration, feel free to contact:
- **Name:** Majd Sasa
- **Email:** Majd.Sasa98@outlook.com
- **GitHub:** (https://github.com/majd182)

---
