#!/usr/bin/env python3
import paho.mqtt.client as mqtt # MQTT client library
import RPi.GPIO as GPIO         # GPIO library for Raspberry Pi
import json                     # For JSON serialization/deserialization
import serial                   # For serial communication with Arduino
import time                     # For time-related functions (e.g., timestamps)
import requests                 # For making HTTP requests (e.g., to ThingsBoard HTTP API)
import threading                # For running MQTT client in a separate thread

# --- Configuration ---
# ThingsBoard MQTT and HTTP API details
THINGSBOARD_HOST = 'thingsboard.cloud'
ACCESS_TOKEN = 'MChdaEdIOWeGZSxmiFS3' # Replace with your actual device access token

# Serial communication with Arduino
SERIAL_PORT = '/dev/ttyACM0' # Typically the port for Arduino on Linux
SERIAL_BAUDRATE = 9600

# ThingsBoard HTTP telemetry upload URL (alternative to MQTT for some data)
thingsboard_url = f'https://thingsboard.cloud/api/v1/{ACCESS_TOKEN}/telemetry'

# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1.0)
    print(f"Successfully connected to serial port {SERIAL_PORT}")
except serial.SerialException as e:
    print(f"Error opening serial port {SERIAL_PORT}: {e}")
    print("Please ensure your Arduino is connected and the correct port is specified.")
    exit(1) # Exit if serial connection cannot be established

# Initial state of GPIO pins (using Broadcom BCM pin numbers)
# NOTE: The provided gpio_state uses BOARD numbering, ensure consistency with RPi.GPIO.setmode()
# Assuming BOARD numbering for consistency with RPi.GPIO.setmode(GPIO.BOARD) later.
gpio_state = {
    7: False, 11: False, 12: False, 13: False, 15: False, 16: False, 18: False,
    22: False, 29: False, 31: False, 32: False, 33: False, 35: False, 36: False,
    37: False, 38: False, 40: False
}

# --- MQTT Callbacks ---

def on_connect(client, userdata, flags, rc):
    """
    Callback function executed when the MQTT client connects to the broker.
    Subscribes to RPC request topic to receive commands from ThingsBoard.
    """
    print('Connected to MQTT broker with result code ' + str(rc))
    # Subscribe to RPC requests for this device
    client.subscribe('v1/devices/me/rpc/request/+')

def on_message(client, userdata, msg):
    """
    Callback function executed when a message is received on a subscribed MQTT topic.
    Handles RPC commands (e.g., getGpioStatus, setGpioStatus) from ThingsBoard.
    """
    print(f'Topic: {msg.topic}\nMessage: {str(msg.payload)}')
    try:
        data = json.loads(msg.payload)
        method = data.get('method') # Using .get() for safer access
        
        if method == 'getGpioStatus':
            client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        elif method == 'setGpioStatus':
            pin = data.get('params', {}).get('pin')
            enabled = data.get('params', {}).get('enabled')
            if pin is not None and enabled is not None:
                set_gpio_status(pin, enabled)
                # Publish updated GPIO status back as RPC response and as device attributes
                client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
                client.publish('v1/devices/me/attributes', get_gpio_status(), 1)
            else:
                print(f"Invalid parameters for setGpioStatus: {data['params']}")
        else:
            print(f"Unknown RPC method: {method}")
    except json.JSONDecodeError:
        print(f"Failed to decode JSON payload: {msg.payload}")
    except Exception as e:
        print(f"An error occurred in on_message: {e}")

# --- GPIO Functions ---

def get_gpio_status():
    """
    Returns the current state of all monitored GPIO pins as a JSON string.
    """
    return json.dumps(gpio_state)

def set_gpio_status(pin, status):
    """
    Sets the state of a specified GPIO pin and updates its status.
    Args:
        pin (int): The GPIO pin number (BOARD numbering).
        status (bool): The desired state (True for HIGH, False for LOW).
    """
    if pin in gpio_state:
        try:
            GPIO.output(pin, GPIO.HIGH if status else GPIO.LOW)
            gpio_state[pin] = status
            print(f"GPIO pin {pin} set to {'HIGH' if status else 'LOW'}")
        except Exception as e:
            print(f"Error setting GPIO pin {pin} to {status}: {e}")
    else:
        print(f"GPIO pin {pin} is not defined in gpio_state.")

# --- Serial Reading and ThingsBoard Uploading ---

def read_serial_data():
    """
    Continuously reads data from the serial port, parses it,
    and uploads it to ThingsBoard.
    """
    print("Starting serial data reader...")
    while True:
        try:
            data = ser.readline().decode('utf-8').strip()
            if data:
                print(f"Received serial data: {data}")
                try:
                    # Split data by 'x' delimiter (as sent by Arduino)
                    sensor_values = [float(value) for value in data.split('x')]
                    if len(sensor_values) >= 5:
                        # Unpack values based on the Arduino sketch's output order:
                        # distance, humidity, temperature, analogValue (light), waterlevel
                        upload_to_thingsboard(*sensor_values[:5])
                    else:
                        print(f"Insufficient values received from serial: {len(sensor_values)} found, 5 expected.")
                except ValueError:
                    print(f"Invalid data format received from serial: {data}. Expected float values separated by 'x'.")
        except serial.SerialException as e:
            print(f"Serial port error: {e}. Reconnecting...")
            time.sleep(5) # Wait before attempting to reconnect
            try:
                ser.close()
                ser.open()
                print("Serial port reconnected.")
            except serial.SerialException as e:
                print(f"Failed to reconnect serial port: {e}. Retrying...")
                time.sleep(10) # Longer wait on repeated failure
        except UnicodeDecodeError:
            print(f"UnicodeDecodeError: Could not decode bytes from serial. Raw data: {ser.readline()}")
        except Exception as e:
            print(f"An unexpected error occurred during serial reading: {e}")
        time.sleep(0.1) # Small delay to prevent busy-waiting

def upload_to_thingsboard(distance, humidity, temperature, light, waterlevel):
    """
    Uploads sensor telemetry data to ThingsBoard using the HTTP API.
    Args:
        distance (float): Distance from ultrasonic sensor.
        humidity (float): Humidity reading.
        temperature (float): Temperature reading.
        light (float): Analog light sensor reading.
        waterlevel (float): Analog water level sensor reading.
    """
    payload = {
        "ts": int(time.time() * 1000), # Timestamp in milliseconds
        "values": {
            "distance": distance,
            "humidity": humidity,
            "temperature": temperature,
            "light": light,
            "waterlevel": waterlevel
        }
    }
    headers = {'Content-Type': 'application/json'} # Specify content type for JSON payload
    try:
        response = requests.post(thingsboard_url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Data uploaded to Thingsboard successfully.")
        else:
            print(f"Failed to upload data to Thingsboard. Status code: {response.status_code}, response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during Thingsboard upload: {e}")

# --- Main Execution ---

if __name__ == '__main__':
    # GPIO setup
    GPIO.setmode(GPIO.BOARD) # Use BOARD numbering scheme for GPIO pins
    # Set all defined GPIO pins as OUTPUT
    for pin in gpio_state:
        try:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW) # Ensure all pins start in LOW state
        except Exception as e:
            print(f"Error setting up GPIO pin {pin}: {e}")

    # MQTT client setup
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(ACCESS_TOKEN) # Authenticate using the access token

    try:
        client.connect(THINGSBOARD_HOST, 1883, 60) # Connect to ThingsBoard MQTT broker
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        # Clean up GPIO and exit if MQTT connection fails
        GPIO.cleanup()
        ser.close()
        exit(1)

    # Start MQTT client loop in a separate thread to handle incoming messages
    threading.Thread(target=client.loop_forever).start()
    print("MQTT client started in background thread.")

    try:
        read_serial_data() # Start reading serial data in the main thread
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Shutting down...")
    except Exception as e:
        print(f"An unhandled error occurred in the main loop: {e}")
    finally:
        # Cleanup resources on exit
        if ser.is_open:
            ser.close()
            print("Serial port closed.")
        GPIO.cleanup() # Release all GPIO resources
        print("GPIO cleaned up.")
        client.disconnect() # Disconnect MQTT client
        print("MQTT client disconnected.")
