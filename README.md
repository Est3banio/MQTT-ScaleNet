# MQTT-ScaleNet: Verteiltes MQTT-System mit Monitoring

In diesem Projekt haben wir ein komplettes verteiltes MQTT-System mit Java- und Python-Komponenten implementiert, die über einen MQTT-Broker kommunizieren. Das System umfasst mehrere Sensor-Publisher, Subscriber, einen dedizierten MQTT-Broker, Visualisierungsfunktionen mit Datenverarbeitung und Protokollierung sowie ein umfassendes Monitoring mit Prometheus und Node Exporter.

## Komponenten

### Kernkomponenten
- **MQTT-Broker**: Eclipse Mosquitto Broker für das Message-Routing
- **Java-Publisher**: Mehrere Java-basierte Sinuswellen-Publisher
- **Python-Sinuswellen-Publisher**: Python-basierter Sinuswellen-Publisher
- **Temperatur-Publisher**: Simuliert Temperaturmessungen mit Tageszyklen
- **Feuchtigkeits-Publisher**: Simuliert Feuchtigkeitsmessungen mit Tageszyklen
- **Datenprozessor**: Kombiniert Temperatur und Luftfeuchtigkeit zur Berechnung von Hitzeindex und Taupunkt
- **Python-Subscriber**: Python-basierter Subscriber, der auf alle Sensor-Topics lauscht
- **MQTT-Logger**: Zeichnet alle MQTT-Nachrichten mit rotierenden Logs auf
- **Grafana**: Visualisierungstool für Echtzeit-Sensordaten
- **MQTT-CLI**: Kommandozeilen-Interface für Tests und Debugging

### Monitoring-Komponenten
- **Prometheus**: Zeitreihen-Datenbank für Metrik-Sammlung und Monitoring
- **Node Exporter**: System-Metrik-Sammler für Host-Level-Monitoring
- **MQTT Exporter**: Metrik-Exporter für Mosquitto-Broker-Statistiken
- **Grafana Dashboards**: Vorkonfigurierte Dashboards für System- und MQTT-Metriken

## Anforderungen

- Docker und Docker Compose
- (Nur für lokale Entwicklung) Java 11+, Maven, Python 3.9+

## Funktionen

- Mehrere Sensortypen, die Daten zu konfigurierbaren Topics veröffentlichen
- Subscriber, die Daten von mehreren Quellen empfangen und verarbeiten
- Datenverarbeitung, die Eingaben kombiniert, um abgeleitete Metriken zu generieren
- Vollständige Nachrichtenprotokollierung mit persistentem Speicher
- Stopp-Befehlsbehandlung für sauberes Herunterfahren von Komponenten
- Containerisierte Bereitstellung mit Docker und Docker Compose
- Persistenter Speicher für MQTT-Nachrichten, Logs und Grafana-Dashboards
- Netzwerkisolierung zwischen Komponenten für erhöhte Sicherheit
- Visualisierungsfunktionen durch Grafana
- Umfassendes Monitoring mit Prometheus, Node Exporter und MQTT Exporter
- Test-Framework zur Überprüfung der Systemfunktionalität

## Systemarchitektur

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Java Sinus     │     │  Python Sinus   │     │  Temperatur     │
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
│  Subscriber       │    │  Datenprozessor  │    │  Feuchtigkeits- │
│                   │    │                  │    │  Publisher      │
└───────────────────┘    └──────────────────┘    └─────────────────┘
                               │      
                               │      
                         ┌─────▼──────────┐     ┌─────────────────┐
                         │  MQTT Logger   │     │  Grafana        │
                         │                │     │  Visualisierung │
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

## Projektstruktur

```
.
├── broker/                       # MQTT-Broker-Konfiguration
│   ├── Dockerfile
│   └── mosquitto.conf
├── python-publisher/             # Python-Sinuswellen-Publisher
│   ├── Dockerfile
│   ├── publisher.py
│   └── requirements.txt
├── python-subscriber/            # Python-Subscriber-Komponente
│   ├── Dockerfile
│   ├── subscriber.py
│   └── requirements.txt
├── python-temp-publisher/        # Temperatur-Publisher
│   ├── Dockerfile
│   ├── temp_publisher.py
│   └── requirements.txt
├── python-humidity-publisher/    # Feuchtigkeits-Publisher
│   ├── Dockerfile
│   ├── humidity_publisher.py
│   └── requirements.txt
├── python-processor/             # Datenprozessor
│   ├── Dockerfile
│   ├── processor.py
│   └── requirements.txt
├── python-logger/                # MQTT-Nachrichten-Logger
│   ├── Dockerfile
│   ├── logger.py
│   └── requirements.txt
├── mqtt-exporter/                # MQTT-Metriken-Exporter
│   └── Dockerfile
├── grafana/                      # Grafana-Konfiguration
│   └── provisioning/            
│       └── datasources/          # Grafana-Datenquellen-Konfiguration
│           └── prometheus.yml    # Prometheus-Datenquelle-Konfiguration
├── src/                          # Java-Publisher-Quellcode
├── Dockerfile                    # Java-Publisher-Dockerfile
├── pom.xml                       # Maven-Konfiguration
├── docker-compose.yml            # Docker-Compose-Konfiguration
├── prometheus.yml                # Prometheus-Konfiguration
├── test-system.sh                # System-Test-Skript
└── README.md
```

## Datenfluss

1. **Sensor-Daten-Publisher**:
   - Java-Publisher generieren Sinuswellendaten
   - Python-Sinus-Publisher generiert Sinuswellendaten
   - Temperatur-Publisher simuliert Temperaturmessungen mit Tageszyklen
   - Feuchtigkeits-Publisher simuliert Feuchtigkeitsmessungen mit Tageszyklen

2. **Message-Broker**:
   - Alle Nachrichten laufen über den MQTT-Broker
   - Mosquitto übernimmt das Nachrichtenrouting zwischen den Komponenten

3. **Datenkonsumenten**:
   - Subscriber lauscht auf Sensor-Topics und zeigt Daten an
   - Datenprozessor kombiniert Temperatur- und Feuchtigkeitsdaten zur Berechnung von:
     - Hitzeindex (gefühlte Temperatur)
     - Taupunkt
   - Logger zeichnet alle MQTT-Nachrichten mit Zeitstempeln auf

4. **Visualisierung**:
   - Grafana verbindet sich mit dem MQTT-Broker, um Echtzeit-Daten anzuzeigen
   - Mehrere Dashboards können für verschiedene Datentypen erstellt werden

5. **Monitoring**:
   - Node Exporter sammelt Systemmetriken (CPU, Speicher, Netzwerk, Festplatte)
   - MQTT Exporter sammelt Mosquitto-Broker-Metriken
   - Prometheus speichert alle Metriken mit Zeitstempeln
   - Grafana visualisiert System- und MQTT-Metriken

## Aufbau und Ausführung des verteilten Systems

### Mit Docker Compose (Empfohlen)

Das gesamte System kann mit Docker Compose erstellt und gestartet werden:

```bash
# Alle Services erstellen und starten
docker-compose up -d --build

# Container-Status prüfen
docker-compose ps

# Alle Services stoppen
docker-compose down

# Alle Services stoppen und Volumes löschen
docker-compose down -v
```

### Systemtests

Ein Test-Skript wird bereitgestellt, um zu überprüfen, ob das System korrekt funktioniert:

```bash
# Sicherstellen, dass das Skript ausführbar ist
chmod +x test-system.sh

# Systemtests ausführen
./test-system.sh
```

Das Test-Skript überprüft:
- Alle Services laufen
- MQTT-Broker-Konnektivität
- Sensordatenveröffentlichung
- Grafana-Verfügbarkeit
- Logger-Funktionalität
- Stopp-Befehlsbehandlung

### Komponentenspezifische Befehle

```bash
# Logs eines bestimmten Services anzeigen
docker-compose logs java-publisher-1
docker-compose logs python-subscriber

# Einen bestimmten Service neu starten
docker-compose restart python-publisher

# Einen Service skalieren (mehr Instanzen hinzufügen)
docker-compose up -d --scale python-publisher=3
```

## Zugriff auf Komponenten

- **MQTT-Broker**: Verfügbar auf Port 1883 für MQTT und 9001 für WebSockets
- **Grafana**: Verfügbar unter http://localhost:3000 (Standardanmeldedaten: admin/admin)
- **Prometheus**: Verfügbar unter http://localhost:9090
- **Node Exporter Metriken**: Verfügbar unter http://localhost:9100/metrics
- **MQTT Exporter Metriken**: Verfügbar unter http://localhost:9234/metrics
- **MQTT CLI**: Zugriff über `docker-compose exec mqtt-cli sh`

## Testen des Systems

### Mit der MQTT CLI

```bash
# Verbindung zum CLI-Container herstellen
docker-compose exec mqtt-cli sh

# Alle Sensor-Topics abonnieren
mqtt sub -h mqtt-broker -t "sensoren/#" -v

# Eine Nachricht an ein bestimmtes Topic senden
mqtt pub -h mqtt-broker -t "sensoren/test" -m "0.123456"

# Stopp-Befehl senden, um einen bestimmten Publisher zu stoppen
mqtt pub -h mqtt-broker -t "feedback/java1" -m "stop"
```

### Mit externen MQTT-Clients

Man kann auch von außerhalb Docker mit Tools wie MQTT Explorer, MQTT.fx oder Mosquitto-Clients eine Verbindung zum Broker herstellen:

```bash
# Abonnieren mit mosquitto_sub
mosquitto_sub -h localhost -t "sensoren/#" -v

# Veröffentlichen mit mosquitto_pub
mosquitto_pub -h localhost -t "feedback/python1" -m "stop"
```

## Visualisierung und Monitoring

### Sensordaten-Visualisierung mit Grafana

1. Grafana unter http://localhost:3000 aufrufen
2. Mit Standardanmeldedaten anmelden (admin/admin)
3. MQTT-Datenquelle hinzufügen:
   - Konfiguration > Datenquellen > Datenquelle hinzufügen
   - "MQTT" auswählen (Plugin bei Bedarf installieren)
   - Broker-URL auf "mqtt-broker:1883" oder "localhost:1883" (bei externem Zugriff) setzen
4. Neues Dashboard erstellen:
   - Panels hinzufügen, um Sensordaten zu visualisieren
   - Abonnements für "sensoren/+" konfigurieren
   - Aktualisierungsrate für Echtzeit-Updates einstellen

### System-Monitoring mit Prometheus und Grafana

1. Prometheus unter http://localhost:9090 aufrufen
   - Targets unter http://localhost:9090/targets ansehen, um sicherzustellen, dass alle Exporter aktiv sind
   - PromQL für direkte Abfragen verwenden
   
2. Vorkonfigurierte Grafana-Dashboards für System-Monitoring verwenden:
   - Node-Exporter-Dashboard für Systemmetriken
   - MQTT-Dashboard für Broker-Metriken
   
3. Benutzerdefinierte Dashboards erstellen:
   - Systemmetriken mit MQTT-Metriken kombinieren
   - Alarme für kritische Schwellenwerte einrichten
   - Anmerkungen für wichtige Ereignisse konfigurieren

## Docker-Volumes

Das System enthält persistente Volumes für:
- `mosquitto-data`: Speichert persistente MQTT-Nachrichten
- `mosquitto-log`: Speichert MQTT-Broker-Logs
- `grafana-storage`: Speichert Grafana-Dashboards und -Konfigurationen
- `mqtt-logs`: Speichert MQTT-Nachrichtenlogs
- `prometheus-data`: Speichert Prometheus-Zeitreihendaten

Diese Volumes stellen sicher, dass Daten auch bei Neustart der Container erhalten bleiben.

## Sicherheitsüberlegungen

Die Standardkonfiguration erlaubt anonymen Zugriff auf den MQTT-Broker, was für die Entwicklung geeignet ist, aber nicht für die Produktion. Für den Produktionseinsatz:

1. MQTT-Authentifizierung konfigurieren (mosquitto.conf bearbeiten)
2. Sichere Verbindungen verwenden (TLS)
3. Netzwerkisolierung für Container anwenden
4. Docker-Sicherheitsoptionen aktualisieren
5. Sichere Passwörter für Grafana und Prometheus festlegen
6. Zugriff auf Monitoring-Endpunkte einschränken

## Skalierung des Systems

Diese Architektur kann auf verschiedene Arten skaliert werden:

1. **Horizontale Skalierung**: Mehr Publisher oder Subscriber durch Skalierung von Diensten hinzufügen
   ```bash
   docker-compose up -d --scale python-publisher=3
   ```

2. **Broker-Clustering**: Mehrere MQTT-Broker in einem Cluster für hohe Verfügbarkeit einrichten
   
3. **Lastverteilung**: Load Balancer vor kritischen Diensten platzieren

4. **Persistenter Speicher**: Externe Datenbanken für langfristige Datenspeicherung verwenden

## Lokale Entwicklung

### Java-Komponente

```bash
# Mit Maven erstellen
mvn clean package

# Lokal ausführen
java -jar target/mqtt-sinus-publisher-1.0-SNAPSHOT-jar-with-dependencies.jar sensoren/local feedback/local
```

### Python-Komponenten

```bash
# Abhängigkeiten installieren
pip install -r python-publisher/requirements.txt

# Publisher ausführen
python python-publisher/publisher.py

# Subscriber ausführen
python python-subscriber/subscriber.py
```

## Umgebungsvariablen

Alle Komponenten unterstützen die Konfiguration über Umgebungsvariablen:

### Kernkomponenten
- `MQTT_BROKER`: MQTT-Broker-Adresse (Standard: mqtt-broker oder localhost:1883)
- `MQTT_PUB_TOPIC`: Topic, in das veröffentlicht werden soll
- `MQTT_SUB_TOPIC`: Topic, das abonniert werden soll
- `MQTT_FEEDBACK_TOPIC`: Topic für Steuerbefehle
- `MQTT_CLIENT_ID`: Eindeutige Client-Kennung

### Monitoring-Komponenten
- Prometheus und Exporter verwenden ihre jeweiligen Konfigurationsdateien für Einstellungen

## Fehlerbehebung

### Häufige Probleme

1. **Container startet nicht**:
   - Logs mit `docker-compose logs <service-name>` überprüfen
   - Netzwerkkonnektivität zwischen Containern überprüfen
   - Sicherstellen, dass erforderliche Volumes existieren

2. **MQTT-Kommunikationsprobleme**:
   - Überprüfen, ob der Broker läuft, mit `docker-compose ps`
   - Broker-Logs mit `docker-compose logs mqtt-broker` überprüfen
   - Konnektivität mit MQTT CLI testen

3. **Monitoring-Probleme**:
   - Prometheus-Targets unter http://localhost:9090/targets überprüfen
   - Exporter-Endpunkte auf Erreichbarkeit prüfen
   - Prometheus-Logs mit `docker-compose logs prometheus` überprüfen

## Mitwirken

Beiträge zu MQTT-ScaleNet sind willkommen! Bitte folgen Sie diesen Schritten:

1. Repository forken
2. Feature-Branch erstellen
3. Änderungen hinzufügen
4. Gründlich testen
5. Pull-Request einreichen

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

## Danksagungen

- Eclipse Mosquitto für den MQTT-Broker
- Prometheus für das Monitoring
- Grafana für die Visualisierung
- Alle Docker-Image-Betreuer