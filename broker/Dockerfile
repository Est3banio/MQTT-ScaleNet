# Use the official Mosquitto image
FROM eclipse-mosquitto:latest

# Copy the Mosquitto configuration file
COPY mosquitto.conf /mosquitto/config/mosquitto.conf

# Create directories for persistence and ensure permissions
RUN mkdir -p /mosquitto/data /mosquitto/log && \
    chmod -R 777 /mosquitto/data /mosquitto/log

# Expose ports
EXPOSE 1883 9001

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]