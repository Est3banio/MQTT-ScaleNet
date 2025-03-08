#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import os
import signal
import sys
import json
import time
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

# MQTT configuration
broker_address = os.environ.get("MQTT_BROKER", "mqtt-broker")
topic_filter = os.environ.get("MQTT_TOPIC_FILTER", "#")  # Subscribe to all topics by default
feedback_topic = os.environ.get("MQTT_FEEDBACK_TOPIC", "feedback/logger")
client_id = os.environ.get("MQTT_CLIENT_ID", "MQTTLogger")

# Logging configuration
log_dir = os.environ.get("LOG_DIR", "/app/logs")
log_file = os.path.join(log_dir, "mqtt_messages.log")
max_log_size = int(os.environ.get("MAX_LOG_SIZE", 10 * 1024 * 1024))  # 10 MB by default
backup_count = int(os.environ.get("BACKUP_COUNT", 5))  # Keep 5 backup files

# Flag to control the logging loop
running = True

# Set up logging
def setup_logging():
    """Configure the logger"""
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)
    
    # Set up file logger with rotation
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_log_size, backupCount=backup_count
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Set up console logger
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

def signal_handler(sig, frame):
    """Handle SIGINT and SIGTERM to gracefully exit"""
    global running
    logger.info("Shutdown signal received. Exiting...")
    running = False

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def on_connect(client, userdata, flags, rc):
    """Called when connected to MQTT broker"""
    if rc == 0:
        logger.info(f"Connected to MQTT broker: {broker_address}")
        # Subscribe to all topics
        client.subscribe(topic_filter)
        logger.info(f"Subscribed to topic filter: {topic_filter}")
        # Subscribe to feedback topic
        client.subscribe(feedback_topic)
        logger.info(f"Subscribed to feedback topic: {feedback_topic}")
    else:
        logger.error(f"Connection failed with code {rc}")

def on_message(client, userdata, message):
    """Handle incoming messages"""
    topic = message.topic
    payload = message.payload.decode('utf-8').strip()
    
    # Process commands on the feedback topic
    if topic == feedback_topic:
        logger.info(f"Received command on {topic}: {payload}")
        if payload.lower() == "stop":
            logger.info("Stop command received. Shutting down...")
            global running
            running = False
        return
    
    # Log the message
    try:
        # Try to parse as JSON for formatted logging
        json_payload = json.loads(payload)
        logger.info(f"Topic: {topic}, Payload: {json.dumps(json_payload, indent=2)}")
    except json.JSONDecodeError:
        # Log as plain text if not JSON
        logger.info(f"Topic: {topic}, Payload: {payload}")

def on_disconnect(client, userdata, rc):
    """Called when disconnected from MQTT broker"""
    logger.info(f"Disconnected with result code {rc}")

# Set up MQTT client
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

try:
    # Connect to broker
    logger.info(f"Connecting to broker: {broker_address}")
    client.connect(broker_address)
    client.loop_start()
    
    # Main loop to keep the script running
    while running:
        time.sleep(1)
    
except KeyboardInterrupt:
    logger.info("Keyboard interrupt received. Exiting...")
except Exception as e:
    logger.error(f"Error: {e}")
finally:
    # Clean up
    client.loop_stop()
    client.disconnect()
    logger.info("Logger stopped and disconnected.")
    sys.exit(0)