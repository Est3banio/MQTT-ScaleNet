#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
import math
import os
import signal
import sys
import random
from datetime import datetime

# MQTT configuration from environment variables or defaults
broker_address = os.environ.get("MQTT_BROKER", "mqtt-broker")
pub_topic = os.environ.get("MQTT_PUB_TOPIC", "sensoren/humidity")
feedback_topic = os.environ.get("MQTT_FEEDBACK_TOPIC", "feedback/humidity")
client_id = os.environ.get("MQTT_CLIENT_ID", "HumidityPublisher")

# Humidity simulation parameters
base_humidity = float(os.environ.get("BASE_HUMIDITY", "60.0"))  # Base humidity in %
day_variation = float(os.environ.get("DAY_VARIATION", "15.0"))  # Daily humidity variation
noise_level = float(os.environ.get("NOISE_LEVEL", "2.0"))  # Random noise level

# Flag to control the publishing loop
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
        # Subscribe to the feedback topic
        client.subscribe(feedback_topic)
        print(f"Subscribed to feedback topic: {feedback_topic}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, message):
    """Handle incoming messages"""
    payload = message.payload.decode('utf-8')
    print(f"Received message on {message.topic}: {payload}")
    
    # Process commands
    if message.topic == feedback_topic:
        if payload.lower() == "stop":
            print("Stop command received. Shutting down...")
            global running
            running = False

def on_disconnect(client, userdata, rc):
    """Called when disconnected from MQTT broker"""
    print(f"Disconnected with result code {rc}")

def simulate_humidity(timestamp):
    """Simulate humidity with daily cycle and random noise
    Humidity is typically higher at night and lower during the day
    """
    # Convert timestamp to hour of day (0-24)
    hour = timestamp.hour + timestamp.minute / 60.0
    
    # Daily humidity cycle: inverse of temperature (higher at night, lower in day)
    daily_factor = -math.sin((hour - 6) * math.pi / 12)  
    
    # Calculate humidity (ensure it stays within reasonable bounds)
    humidity = base_humidity + day_variation * daily_factor + random.uniform(-noise_level, noise_level)
    humidity = max(30, min(95, humidity))  # Keep humidity between 30% and 95%
    
    return round(humidity, 1)

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
    
    # Main publishing loop
    while running:
        # Get current time and simulate humidity
        now = datetime.now()
        humidity = simulate_humidity(now)
        
        # Create payload with humidity value
        payload = f"{humidity:.1f}"
        
        # Publish to topic
        client.publish(pub_topic, payload)
        print(f"Published to {pub_topic}: {payload}% at {now.strftime('%H:%M:%S')}")
        
        # Wait before next reading
        time.sleep(1)
    
except KeyboardInterrupt:
    print("Keyboard interrupt received. Exiting...")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Clean up
    client.loop_stop()
    client.disconnect()
    print("Publisher stopped and disconnected.")
    sys.exit(0)