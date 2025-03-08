FROM openjdk:11-slim

WORKDIR /app

# Copy maven files first for better layer caching
COPY pom.xml /app/
# Create the maven wrapper directory
RUN mkdir -p /app/.mvn/wrapper

# Copy only necessary project files
COPY src /app/src/

# Install Maven
RUN apt-get update && \
    apt-get install -y maven && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Build the application
RUN mvn clean package

# Make the application more secure by running as non-root
RUN useradd -m javauser
USER javauser

# Set environment variables with default values that can be overridden
ENV MQTT_BROKER=tcp://mosquitto:1883
ENV MQTT_PUB_TOPIC=sensoren/java1
ENV MQTT_SUB_TOPIC=feedback/java1

# Command to run the application
CMD ["java", "-jar", "target/mqtt-sinus-publisher-1.0-SNAPSHOT-jar-with-dependencies.jar"]