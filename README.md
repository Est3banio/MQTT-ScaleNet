# MQTT Distributed System

This project demonstrates a complete distributed MQTT system with Java and Python components publishing and subscribing to an MQTT broker. The system includes multiple sensor publishers, subscribers, a dedicated MQTT broker, and visualization capabilities with data processing and logging.

## Components

- **MQTT Broker**: Eclipse Mosquitto broker for message routing
- **Java Publishers**: Multiple Java-based sine wave publishers 
- **Python Sine Publisher**: Python-based sine wave publisher
- **Temperature Publisher**: Simulates temperature readings with daily cycles
- **Humidity Publisher**: Simulates humidity readings with daily cycles
- **Data Processor**: Combines temperature and humidity to calculate heat index and dew point
- **Python Subscriber**: Python-based subscriber that listens to all sensor topics
- **MQTT Logger**: Records all MQTT messages with rotating logs
- **Grafana**: Visualization tool for real-time sensor data
- **MQTT CLI**: Command-line interface for testing and debugging

## Requirements

- Docker and Docker Compose
- (For local development only) Java 11+, Maven, Python 3.9+

## Features

- Multiple sensor types publishing data to configurable topics
- Subscribers receiving and processing data from multiple sources
- Data processing that combines inputs to generate derived metrics
- Complete message logging with persistent storage
- Stop command handling for graceful shutdown of components
- Containerized deployment with Docker and Docker Compose
- Persistent storage for MQTT messages, logs, and Grafana dashboards
- Network isolation between components for security
- Visualization capabilities through Grafana
- Testing framework to verify system functionality

## System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Java Sine      │     │  Python Sine    │     │  Temperature    │
│  Publishers     │     │  Publisher      │     │  Publisher      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                       │
         │                      │                       │
         │                      ▼                       │
         │               ┌─────────────────┐            │
         └──────────────►│  MQTT Broker    │◄───────────┘
                         │  (Mosquitto)    │
         ┌──────────────►│                 │◄───────────┐
         │               └─────────────────┘            │
         │                       ▲                      │
         │                       │                      │
         │                       │                      │
┌────────▼──────────┐    ┌──────▼───────────┐    ┌─────▼───────────┐
│  Subscriber       │    │  Data Processor  │    │  Humidity       │
│                   │    │                  │    │  Publisher      │
└───────────────────┘    └──────────────────┘    └─────────────────┘
                               │      
                               │      
                         ┌─────▼──────────┐     ┌─────────────────┐
                         │  MQTT Logger   │     │  Grafana        │
                         │                │     │  Visualization  │
                         └────────────────┘     └─────────────────┘
```

## Project Structure

```
.
├── broker/                       # MQTT broker configuration
│   ├── Dockerfile
│   └── mosquitto.conf
├── python-publisher/             # Python sine wave publisher
│   ├── Dockerfile
│   ├── publisher.py
│   └── requirements.txt
├── python-subscriber/            # Python subscriber component
│   ├── Dockerfile
│   ├── subscriber.py
│   └── requirements.txt
├── python-temp-publisher/        # Temperature publisher
│   ├── Dockerfile
│   ├── temp_publisher.py
│   └── requirements.txt
├── python-humidity-publisher/    # Humidity publisher
│   ├── Dockerfile
│   ├── humidity_publisher.py
│   └── requirements.txt
├── python-processor/             # Data processor 
│   ├── Dockerfile
│   ├── processor.py
│   └── requirements.txt
├── python-logger/                # MQTT message logger
│   ├── Dockerfile
│   ├── logger.py
│   └── requirements.txt
├── src/                          # Java publisher source code
├── Dockerfile                    # Java publisher Dockerfile
├── pom.xml                       # Maven configuration
├── docker-compose.yml            # Docker Compose configuration
├── test-system.sh                # System testing script
└── README.md
```

## Data Flow

1. **Sensor Data Publishers**:
   - Java publishers generate sine wave data
   - Python sine publisher generates sine wave data
   - Temperature publisher simulates temperature readings with daily cycles
   - Humidity publisher simulates humidity readings with daily cycles

2. **Message Broker**:
   - All messages pass through the MQTT broker
   - Mosquitto handles message routing between components

3. **Data Consumers**:
   - Subscriber listens to sensor topics and displays data
   - Data processor combines temperature and humidity data to calculate:
     - Heat index (feels-like temperature)
     - Dew point
   - Logger records all MQTT messages with timestamps

4. **Visualization**:
   - Grafana connects to MQTT broker to display real-time data
   - Multiple dashboards can be created for different data types

## Building and Running the Distributed System

### Using Docker Compose (Recommended)

The entire system can be built and launched with Docker Compose:

```bash
# Build and start all services
docker-compose up -d --build

# Check container status
docker-compose ps

# Stop all services
docker-compose down

# Stop all services and remove volumes
docker-compose down -v
```

### System Testing

A test script is provided to verify the system is working correctly:

```bash
# Make sure the script is executable
chmod +x test-system.sh

# Run the system tests
./test-system.sh
```

The test script checks:
- All services are running
- MQTT broker connectivity
- Sensor data publishing
- Grafana availability
- Logger functionality
- Stop command handling

### Component-Specific Commands

```bash
# View logs of a specific service
docker-compose logs java-publisher-1
docker-compose logs python-subscriber

# Restart a specific service
docker-compose restart python-publisher

# Scale a service (add more instances)
docker-compose up -d --scale python-publisher=3
```

## Accessing Components

- **MQTT Broker**: Available on port 1883 for MQTT and 9001 for WebSockets
- **Grafana**: Available at http://localhost:3000 (default credentials: admin/admin)
- **MQTT CLI**: Access via `docker-compose exec mqtt-cli sh`

## Testing the System

### Using the MQTT CLI

```bash
# Connect to the CLI container
docker-compose exec mqtt-cli sh

# Subscribe to all sensor topics
mqtt sub -h mqtt-broker -t "sensoren/#" -v

# Send a message to a specific topic
mqtt pub -h mqtt-broker -t "sensoren/test" -m "0.123456"

# Send stop command to stop a specific publisher
mqtt pub -h mqtt-broker -t "feedback/java1" -m "stop"
```

### Using External MQTT Clients

You can also connect to the broker from outside Docker using tools like MQTT Explorer, MQTT.fx, or Mosquitto clients:

```bash
# Subscribe using mosquitto_sub
mosquitto_sub -h localhost -t "sensoren/#" -v

# Publish using mosquitto_pub
mosquitto_pub -h localhost -t "feedback/python1" -m "stop"
```

## Visualizing Data with Grafana

1. Access Grafana at http://localhost:3000
2. Login with default credentials (admin/admin)
3. Add the MQTT data source:
   - Go to Configuration > Data Sources > Add data source
   - Select "MQTT" (install plugin if needed)
   - Set broker URL to "mqtt-broker:1883" or "localhost:1883" (if accessing externally)
4. Create a new dashboard:
   - Add panels to visualize sensor data
   - Configure subscriptions to "sensoren/+"
   - Set refresh rate for real-time updates

## Docker Volumes

The system includes persistent volumes for:
- `mosquitto-data`: Stores persistent MQTT messages
- `mosquitto-log`: Stores MQTT broker logs
- `grafana-storage`: Stores Grafana dashboards and configurations

These volumes ensure data is preserved even if containers are restarted.

## Security Considerations

The default configuration allows anonymous access to the MQTT broker, which is suitable for development but not for production. For production use:

1. Configure MQTT authentication (edit mosquitto.conf)
2. Use secure connections (TLS)
3. Apply network isolation for containers
4. Update Docker security options
5. Set secure passwords for Grafana

## Local Development

### Java Component

```bash
# Build with Maven
mvn clean package

# Run locally
java -jar target/mqtt-sinus-publisher-1.0-SNAPSHOT-jar-with-dependencies.jar sensoren/local feedback/local
```

### Python Components

```bash
# Install dependencies
pip install -r python-publisher/requirements.txt

# Run publisher
python python-publisher/publisher.py

# Run subscriber
python python-subscriber/subscriber.py
```

## Environment Variables

All components support configuration through environment variables:

- `MQTT_BROKER`: MQTT broker address (default: mqtt-broker or localhost:1883)
- `MQTT_PUB_TOPIC`: Topic to publish to
- `MQTT_SUB_TOPIC`: Topic to subscribe to
- `MQTT_FEEDBACK_TOPIC`: Topic for control commands
- `MQTT_CLIENT_ID`: Unique client identifier