#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import os
import signal
import sys
import json
import time

# MQTT configuration from environment variables or defaults
broker_address = os.environ.get("MQTT_BROKER", "mqtt-broker")
sub_topic = os.environ.get("MQTT_SUB_TOPIC", "sensoren/+")
feedback_topic = os.environ.get("MQTT_FEEDBACK_TOPIC", "feedback/python1")
client_id = os.environ.get("MQTT_CLIENT_ID", "PythonSubscriber")

# Flag to control the subscription loop
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
        # Subscribe to the topic(s)
        client.subscribe(sub_topic)
        print(f"Subscribed to: {sub_topic}")
        # Also subscribe to a feedback topic to receive commands
        client.subscribe(feedback_topic)
        print(f"Subscribed to feedback topic: {feedback_topic}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, message):
    """Called when a message is received"""
    topic = message.topic
    payload = message.payload.decode('utf-8')
    
    # Handle feedback commands (like "stop")
    if topic == feedback_topic:
        print(f"Received command on {topic}: {payload}")
        if payload.lower() == "stop":
            print("Stop command received. Shutting down...")
            global running
            running = False
    else:
        # Process regular data messages
        print(f"Received on {topic}: {payload}")
        
        # Here you could process the data further:
        # - Store in a database
        # - Perform calculations
        # - Forward to another service

def on_disconnect(client, userdata, rc):
    """Called when disconnected from MQTT broker"""
    print(f"Disconnected with result code {rc}")

# Set up MQTT client
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

try:
    # Connect to broker
    print(f"Connecting to broker: {broker_address}")
    client.connect(broker_address)
    
    # Start the network loop
    client.loop_start()
    
    # Keep running until signaled to stop
    while running:
        time.sleep(1)
    
except KeyboardInterrupt:
    print("Keyboard interrupt received. Exiting...")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Clean up
    client.loop_stop()
    client.disconnect()
    print("Subscriber stopped and disconnected.")
    sys.exit(0)