#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
import math
import os
import signal
import sys
import json
from datetime import datetime

# MQTT configuration from environment variables or defaults
broker_address = os.environ.get("MQTT_BROKER", "mqtt-broker")
temp_topic = os.environ.get("MQTT_TEMP_TOPIC", "sensoren/temperature")
humidity_topic = os.environ.get("MQTT_HUMIDITY_TOPIC", "sensoren/humidity")
output_topic = os.environ.get("MQTT_OUTPUT_TOPIC", "sensoren/processed")
feedback_topic = os.environ.get("MQTT_FEEDBACK_TOPIC", "feedback/processor")
client_id = os.environ.get("MQTT_CLIENT_ID", "DataProcessor")

# Data storage
last_temp = None
last_humidity = None
publish_interval = float(os.environ.get("PUBLISH_INTERVAL", "1.0"))  # seconds
last_publish_time = 0

# Flag to control the processing loop
running = True

def signal_handler(sig, frame):
    """Handle SIGINT and SIGTERM to gracefully exit"""
    global running
    print("Shutdown signal received. Exiting...")
    running = False

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def on_connect(client, userdata, flags, rc):
    """Called when connected to MQTT broker"""
    if rc == 0:
        print(f"Connected to MQTT broker: {broker_address}")
        # Subscribe to input topics
        client.subscribe(temp_topic)
        print(f"Subscribed to temperature topic: {temp_topic}")
        client.subscribe(humidity_topic)
        print(f"Subscribed to humidity topic: {humidity_topic}")
        # Subscribe to feedback topic
        client.subscribe(feedback_topic)
        print(f"Subscribed to feedback topic: {feedback_topic}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, message):
    """Handle incoming messages"""
    topic = message.topic
    payload = message.payload.decode('utf-8').strip()
    
    # Process commands
    if topic == feedback_topic:
        print(f"Received command on {topic}: {payload}")
        if payload.lower() == "stop":
            print("Stop command received. Shutting down...")
            global running
            running = False
        return
        
    # Process sensor data
    try:
        if topic == temp_topic:
            global last_temp
            last_temp = float(payload)
            print(f"Received temperature: {last_temp}°C")
        elif topic == humidity_topic:
            global last_humidity
            last_humidity = float(payload)
            print(f"Received humidity: {last_humidity}%")
    except ValueError as e:
        print(f"Error parsing data from {topic}: {e}")

def on_disconnect(client, userdata, rc):
    """Called when disconnected from MQTT broker"""
    print(f"Disconnected with result code {rc}")

def calculate_heat_index(temp_c, humidity):
    """Calculate the heat index (feels-like temperature) in Celsius"""
    # Convert to Fahrenheit for the standard heat index formula
    temp_f = (temp_c * 9/5) + 32
    
    # Simple formula for heat index
    hi_f = 0.5 * (temp_f + 61.0 + ((temp_f - 68.0) * 1.2) + (humidity * 0.094))
    
    # Use more complex formula if heat index is above 80°F
    if hi_f > 80:
        hi_f = -42.379 + 2.04901523 * temp_f + 10.14333127 * humidity
        hi_f = hi_f - 0.22475541 * temp_f * humidity - 6.83783e-3 * temp_f**2
        hi_f = hi_f - 5.481717e-2 * humidity**2 + 1.22874e-3 * temp_f**2 * humidity
        hi_f = hi_f + 8.5282e-4 * temp_f * humidity**2 - 1.99e-6 * temp_f**2 * humidity**2
    
    # Convert back to Celsius
    hi_c = (hi_f - 32) * 5/9
    return round(hi_c, 1)

def calculate_dew_point(temp_c, humidity):
    """Calculate the dew point in Celsius"""
    a = 17.27
    b = 237.7
    
    # Calculate the gamma term
    gamma = ((a * temp_c) / (b + temp_c)) + math.log(humidity/100.0)
    
    # Calculate dew point
    dew_point = (b * gamma) / (a - gamma)
    return round(dew_point, 1)

# Set up MQTT client
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

try:
    # Connect to broker
    print(f"Connecting to broker: {broker_address}")
    client.connect(broker_address)
    client.loop_start()
    
    # Main processing loop
    while running:
        current_time = time.time()
        
        # Process and publish data if we have both temperature and humidity
        if (last_temp is not None and last_humidity is not None and 
            current_time - last_publish_time >= publish_interval):
            
            # Calculate derived metrics
            heat_index = calculate_heat_index(last_temp, last_humidity)
            dew_point = calculate_dew_point(last_temp, last_humidity)
            
            # Create payload
            data = {
                "temperature": last_temp,
                "humidity": last_humidity,
                "heat_index": heat_index,
                "dew_point": dew_point,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            json_payload = json.dumps(data)
            
            # Publish processed data
            client.publish(output_topic, json_payload)
            print(f"Published processed data: Temperature={last_temp}°C, Humidity={last_humidity}%, "
                  f"Heat Index={heat_index}°C, Dew Point={dew_point}°C")
            
            last_publish_time = current_time
        
        time.sleep(0.1)  # Small sleep to prevent CPU hogging
    
except KeyboardInterrupt:
    print("Keyboard interrupt received. Exiting...")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Clean up
    client.loop_stop()
    client.disconnect()
    print("Processor stopped and disconnected.")
    sys.exit(0)