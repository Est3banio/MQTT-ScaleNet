# MQTT-ScaleNet: Distributed MQTT System with Monitoring

This project implements a complete distributed MQTT system with Java and Python components communicating through an MQTT broker. The system includes multiple sensor publishers, subscribers, a dedicated MQTT broker, visualization features with data processing and logging, as well as comprehensive monitoring with Prometheus and Node Exporter.

## Components

### Core Components

- **MQTT Broker**: Eclipse Mosquitto broker for message routing
- **Java Publisher**: Multiple Java-based sine wave publishers
- **Python Sine Wave Publisher**: Python-based sine wave publisher
- **Temperature Publisher**: Simulates temperature measurements with daily cycles
- **Humidity Publisher**: Simulates humidity measurements with daily cycles
- **Data Processor**: Combines temperature and humidity to calculate heat index and dew point
- **Python Subscriber**: Python-based subscriber listening to all sensor topics
- **MQTT Logger**: Records all MQTT messages with rotating logs
- **Grafana**: Visualization tool for real-time sensor data
- **MQTT CLI**: Command-line interface for testing and debugging

### Monitoring Components

- **Prometheus**: Time-series database for metric collection and monitoring
- **Node Exporter**: System metric collector for host-level monitoring
- **MQTT Exporter**: Metric exporter for Mosquitto broker statistics
- **Grafana Dashboards**: Pre-configured dashboards for system and MQTT metrics

## Requirements

- Docker and Docker Compose
- (Only for local development) Java 11+, Maven, Python 3.9+

## Features

- Multiple sensor types publishing data to configurable topics
- Subscribers receiving and processing data from multiple sources
- Data processing combining inputs to generate derived metrics
- Complete message logging with persistent storage
- Stop command handling for clean component shutdown
- Containerized deployment with Docker and Docker Compose
- Persistent storage for MQTT messages, logs, and Grafana dashboards
- Network isolation between components for increased security
- Visualization capabilities through Grafana
- Comprehensive monitoring with Prometheus, Node Exporter, and MQTT Exporter
- Test framework to verify system functionality

## System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Java Sine      │     │  Python Sine    │     │  Temperature    │
│  Publisher      │     │  Publisher      │     │  Publisher      │
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
                                                       ▲
                                                       │
                      ┌────────────────┐               │
                      │  MQTT Exporter │───────────────┤
                      └────────────────┘               │
                              ▲                        │
                              │                        │
               ┌──────────────┴─────────┐              │
               │                        │              │
        ┌──────▼──────┐         ┌──────▼──────┐        │
        │ Prometheus  │─────────►Node Exporter│────────┘
        └─────────────┘         └─────────────┘
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
├── mqtt-exporter/                # MQTT metrics exporter
│   └── Dockerfile
├── grafana/                      # Grafana configuration
│   └── provisioning/
│       └── datasources/          # Grafana data sources configuration
│           └── prometheus.yml    # Prometheus data source configuration
├── src/                          # Java publisher source code
├── Dockerfile                    # Java publisher Dockerfile
├── pom.xml                       # Maven configuration
├── docker-compose.yml            # Docker Compose configuration
├── prometheus.yml                # Prometheus configuration
├── test-system.sh                # System test script
└── README.md
```

## Data Flow

1. **Sensor Data Publishers**:

   - Java publisher generates sine wave data
   - Python sine publisher generates sine wave data
   - Temperature publisher simulates temperature measurements with daily cycles
   - Humidity publisher simulates humidity measurements with daily cycles

2. **Message Broker**:

   - All messages flow through the MQTT broker
   - Mosquitto handles message routing between components

3. **Data Consumers**:

   - Subscriber listens to sensor topics and displays data
   - Data processor combines temperature and humidity data to calculate:
     - Heat index (perceived temperature)
     - Dew point
   - Logger records all MQTT messages with timestamps

4. **Visualization**:

   - Grafana connects to the MQTT broker to display real-time data
   - Multiple dashboards can be created for different data types

5. **Monitoring**:
   - Node Exporter collects system metrics (CPU, memory, network, disk)
   - MQTT Exporter collects Mosquitto broker metrics
   - Prometheus stores all metrics with timestamps
   - Grafana visualizes system and MQTT metrics

## Building and Running the Distributed System

### Using Docker Compose (Recommended)

The entire system can be built and started with Docker Compose:

```bash
# Build and start all services
docker-compose up -d --build

# Check container status
docker-compose ps

# Stop all services
docker-compose down

# Stop all services and delete volumes
docker-compose down -v
```

### System Tests

A test script is provided to verify if the system is functioning correctly:

```bash
# Ensure the script is executable
chmod +x test-system.sh

# Run system tests
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
# View logs for a specific service
docker-compose logs java-publisher-1
docker-compose logs python-subscriber

# Restart a specific service
docker-compose restart python-publisher

# Scale a service (add more instances)
docker-compose up -d --scale python-publisher=3
```

## Accessing Components

- **MQTT Broker**: Available on port 1883 for MQTT and 9001 for WebSockets
- **Grafana**: Available at <http://localhost:3000> (default credentials: admin/admin)
- **Prometheus**: Available at <http://localhost:9090>
- **Node Exporter Metrics**: Available at <http://localhost:9100/metrics>
- **MQTT Exporter Metrics**: Available at <http://localhost:9234/metrics>
- **MQTT CLI**: Access via `docker-compose exec mqtt-cli sh`

## Testing the System

### Using the MQTT CLI

```bash
# Connect to the CLI container
docker-compose exec mqtt-cli sh

# Subscribe to all sensor topics
mqtt sub -h mqtt-broker -t "sensors/#" -v

# Send a message to a specific topic
mqtt pub -h mqtt-broker -t "sensors/test" -m "0.123456"

# Send stop command to stop a specific publisher
mqtt pub -h mqtt-broker -t "feedback/java1" -m "stop"
```

### Using External MQTT Clients

You can also connect to the broker from outside Docker using tools like MQTT Explorer, MQTT.fx, or Mosquitto clients:

```bash
# Subscribe using mosquitto_sub
mosquitto_sub -h localhost -t "sensors/#" -v

# Publish using mosquitto_pub
mosquitto_pub -h localhost -t "feedback/python1" -m "stop"
```

## Visualization and Monitoring

### Sensor Data Visualization with Grafana

1. Access Grafana at <http://localhost:3000>
2. Log in with default credentials (admin/admin)
3. Add MQTT data source:
   - Configuration > Data Sources > Add data source
   - Select "MQTT" (install plugin if needed)
   - Set broker URL to "mqtt-broker:1883" or "localhost:1883" (for external access)
4. Create a new dashboard:
   - Add panels to visualize sensor data
   - Configure subscriptions for "sensors/+"
   - Set refresh rate for real-time updates

### System Monitoring with Prometheus and Grafana

1. Access Prometheus at <http://localhost:9090>
   - View targets at <http://localhost:9090/targets> to ensure all exporters are active
   - Use PromQL for direct queries
2. Use pre-configured Grafana dashboards for system monitoring:
   - Node Exporter dashboard for system metrics
   - MQTT dashboard for broker metrics
3. Create custom dashboards:
   - Combine system metrics with MQTT metrics
   - Set up alerts for critical thresholds
   - Configure annotations for important events

## Docker Volumes

The system includes persistent volumes for:

- `mosquitto-data`: Stores persistent MQTT messages
- `mosquitto-log`: Stores MQTT broker logs
- `grafana-storage`: Stores Grafana dashboards and configurations
- `mqtt-logs`: Stores MQTT message logs
- `prometheus-data`: Stores Prometheus time-series data

These volumes ensure data persists even when containers are restarted.

## Security Considerations

The default configuration allows anonymous access to the MQTT broker, which is suitable for development but not for production. For production use:

1. Configure MQTT authentication (edit mosquitto.conf)
2. Use secure connections (TLS)
3. Apply network isolation for containers
4. Update Docker security options
5. Set secure passwords for Grafana and Prometheus
6. Restrict access to monitoring endpoints

## Scaling the System

This architecture can be scaled in various ways:

1. **Horizontal Scaling**: Add more publishers or subscribers by scaling services

   ```bash
   docker-compose up -d --scale python-publisher=3
   ```

2. **Broker Clustering**: Set up multiple MQTT brokers in a cluster for high availability
3. **Load Balancing**: Place load balancers in front of critical services

4. **Persistent Storage**: Use external databases for long-term data storage

## Local Development

### Java Component

```bash
# Build with Maven
mvn clean package

# Run locally
java -jar target/mqtt-sinus-publisher-1.0-SNAPSHOT-jar-with-dependencies.jar sensors/local feedback/local
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

### Core Components

- `MQTT_BROKER`: MQTT broker address (default: mqtt-broker or localhost:1883)
- `MQTT_PUB_TOPIC`: Topic to publish to
- `MQTT_SUB_TOPIC`: Topic to subscribe to
- `MQTT_FEEDBACK_TOPIC`: Topic for control commands
- `MQTT_CLIENT_ID`: Unique client identifier

### Monitoring Components

- Prometheus and exporters use their respective configuration files for settings

## Troubleshooting

### Common Issues

1. **Container won't start**:

   - Check logs with `docker-compose logs <service-name>`
   - Verify network connectivity between containers
   - Ensure required volumes exist

2. **MQTT communication issues**:

   - Check if the broker is running with `docker-compose ps`
   - Check broker logs with `docker-compose logs mqtt-broker`
   - Test connectivity with MQTT CLI

3. **Monitoring issues**:
   - Check Prometheus targets at <http://localhost:9090/targets>
   - Verify exporter endpoints are reachable
   - Check Prometheus logs with `docker-compose logs prometheus`

## Contributing

Contributions to MQTT-ScaleNet are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Eclipse Mosquitto for the MQTT broker
- Prometheus for monitoring
- Grafana for visualization
- All Docker image maintainers

