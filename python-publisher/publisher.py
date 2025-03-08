#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
import math
import os
import signal
import sys

# MQTT configuration from environment variables or defaults
broker_address = os.environ.get("MQTT_BROKER", "mqtt-broker")
pub_topic = os.environ.get("MQTT_PUB_TOPIC", "sensoren/python1")
client_id = os.environ.get("MQTT_CLIENT_ID", "PythonPublisher")

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
    else:
        print(f"Connection failed with code {rc}")

def on_disconnect(client, userdata, rc):
    """Called when disconnected from MQTT broker"""
    print(f"Disconnected with result code {rc}")

# Set up MQTT client
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect

try:
    # Connect to broker
    print(f"Connecting to broker: {broker_address}")
    client.connect(broker_address)
    client.loop_start()
    
    # Main publishing loop
    counter = 0.0
    while running:
        # Calculate sine value
        value = math.sin(counter)
        payload = f"{value:.6f}"
        
        # Publish to topic
        client.publish(pub_topic, payload)
        print(f"Published to {pub_topic}: {payload}")
        
        # Increment counter and wait
        counter += 0.1
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