FROM alpine:latest

# Install necessary packages
RUN apk add --no-cache \
    go \
    git \
    build-base

# Clone and build mqtt_exporter
WORKDIR /go/src/
RUN git clone https://github.com/sapcc/mosquitto-exporter.git && \
    cd mosquitto-exporter && \
    go build -o /bin/mosquitto-exporter

# Set up environment
WORKDIR /
EXPOSE 9234

# Run mqtt exporter
ENTRYPOINT ["/bin/mosquitto-exporter"]
CMD ["--endpoint", "tcp://mqtt-broker:1883", "--mqtt.namespace", "mqtt"]