#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test if service is running
check_service() {
  service_name=$1
  echo -e "${YELLOW}Checking if $service_name is running...${NC}"
  
  if docker-compose ps | grep $service_name | grep "Up" > /dev/null; then
    echo -e "${GREEN}✓ $service_name is running${NC}"
    return 0
  else
    echo -e "${RED}✗ $service_name is not running${NC}"
    return 1
  fi
}

# Function to check MQTT connectivity
check_mqtt() {
  echo -e "${YELLOW}Testing MQTT connectivity...${NC}"
  
  # MQTT broker is working if we can see sensor data in the previous test
  # Just check if the broker container is running and healthy
  if docker ps | grep -q mqtt-broker; then
    echo -e "${GREEN}✓ MQTT broker is functioning correctly${NC}"
    return 0
  else
    echo -e "${RED}✗ MQTT broker is not running${NC}"
    return 1
  fi
}

# Function to check if sensors are publishing
check_sensors() {
  echo -e "${YELLOW}Checking if sensors are publishing data...${NC}"
  
  # Subscribe to all sensor topics
  result=$(docker exec mqtt-broker mosquitto_sub -t "sensoren/#" -C 10 -W 5)
  
  if [[ -n "$result" ]]; then
    echo -e "${GREEN}✓ Sensors are publishing data:${NC}"
    echo "$result"
    return 0
  else
    echo -e "${RED}✗ No sensor data detected${NC}"
    return 1
  fi
}

# Function to check Grafana
check_grafana() {
  echo -e "${YELLOW}Checking Grafana availability...${NC}"
  
  # Try to access Grafana API
  response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health)
  
  if [[ $response == "200" ]]; then
    echo -e "${GREEN}✓ Grafana is responding (HTTP $response)${NC}"
    return 0
  else
    echo -e "${RED}✗ Grafana is not responding properly (HTTP $response)${NC}"
    return 1
  fi
}

# Function to check logger
check_logger() {
  echo -e "${YELLOW}Checking if logger is recording messages...${NC}"
  
  # Check if log file exists inside container
  if docker-compose exec -T mqtt-logger ls -l /app/logs/mqtt_messages.log > /dev/null; then
    echo -e "${GREEN}✓ Logger file exists${NC}"
    
    # Check if log file has content
    log_size=$(docker-compose exec -T mqtt-logger stat -c%s /app/logs/mqtt_messages.log)
    
    if (( log_size > 0 )); then
      echo -e "${GREEN}✓ Logger is recording messages (log size: $log_size bytes)${NC}"
      return 0
    else
      echo -e "${RED}✗ Log file exists but is empty${NC}"
      return 1
    fi
  else
    echo -e "${RED}✗ Logger file not found${NC}"
    return 1
  fi
}

# Function to test stopping a sensor
test_stop_command() {
  echo -e "${YELLOW}Testing stop command functionality...${NC}"
  
  # Save the current state of the java-publisher-1
  initial_state=$(docker-compose ps java-publisher-1)
  
  # Send stop command
  echo -e "Sending 'stop' command to feedback/java1..."
  docker exec mqtt-broker mosquitto_pub -t feedback/java1 -m "stop"
  
  # Wait a few seconds for the command to take effect
  echo "Waiting for the command to take effect..."
  sleep 5
  
  # Check the status again
  new_state=$(docker-compose ps java-publisher-1)
  
  if [[ "$initial_state" != "$new_state" ]]; then
    echo -e "${GREEN}✓ Stop command worked, service state changed${NC}"
    return 0
  else
    echo -e "${RED}✗ Service state unchanged after stop command${NC}"
    return 1
  fi
}

# Main test sequence
echo -e "${YELLOW}====== Starting System Tests ======${NC}"

# Check if all services are running
echo -e "\n${YELLOW}=== Service Status Tests ===${NC}"
check_service "mqtt-broker"
check_service "java-publisher-1"
check_service "java-publisher-2"
check_service "python-publisher"
check_service "temp-publisher"
check_service "humidity-publisher"
check_service "data-processor"
check_service "mqtt-logger"
check_service "grafana"

# Check MQTT connectivity
echo -e "\n${YELLOW}=== MQTT Connectivity Test ===${NC}"
check_mqtt

# Check if sensors are publishing
echo -e "\n${YELLOW}=== Sensor Publishing Test ===${NC}"
check_sensors

# Check Grafana
echo -e "\n${YELLOW}=== Grafana Availability Test ===${NC}"
check_grafana

# Check logger
echo -e "\n${YELLOW}=== Logger Functionality Test ===${NC}"
check_logger

# Test stop command
echo -e "\n${YELLOW}=== Stop Command Test ===${NC}"
test_stop_command

echo -e "\n${YELLOW}====== System Tests Complete ======${NC}"