import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import java.util.UUID;

public class MqttSinusPublisher {
    private static final String DEFAULT_BROKER = "tcp://localhost:1883";
    private static final String DEFAULT_PUB_TOPIC = "sensoren/java1";
    private static final String DEFAULT_SUB_TOPIC = "feedback/java1";
    
    private static boolean running = true;
    
    public static void main(String[] args) {
        // Get MQTT broker from environment variable or use default
        String broker = System.getenv("MQTT_BROKER");
        if (broker == null || broker.isEmpty()) {
            broker = DEFAULT_BROKER;
        }
        System.out.println("Using MQTT broker: " + broker);
        // Determine publish and subscribe topics from command-line args, env vars, or defaults
        String pubTopic = DEFAULT_PUB_TOPIC;
        String subTopic = DEFAULT_SUB_TOPIC;
        
        if (args.length >= 2) {
            // Command-line arguments provided
            pubTopic = args[0];
            subTopic = args[1];
            System.out.println("Using command-line arguments for topics");
        } else if (args.length == 1) {
            // Only publish topic provided
            pubTopic = args[0];
            System.out.println("Using command-line argument for publish topic and default for subscribe topic");
        } else {
            // Check environment variables
            String envPubTopic = System.getenv("MQTT_PUB_TOPIC");
            String envSubTopic = System.getenv("MQTT_SUB_TOPIC");
            
            if (envPubTopic != null && !envPubTopic.isEmpty()) {
                pubTopic = envPubTopic;
                System.out.println("Using environment variable for publish topic");
            }
            
            if (envSubTopic != null && !envSubTopic.isEmpty()) {
                subTopic = envSubTopic;
                System.out.println("Using environment variable for subscribe topic");
            }
        }
        
        System.out.println("Publishing to: " + pubTopic);
        System.out.println("Subscribing to: " + subTopic);
        
        // Generate a unique client ID to allow multiple instances
        String clientId = "JavaSinusPublisher-" + UUID.randomUUID().toString();
        
        try {
            // Set up MQTT client with memory persistence instead of file persistence
            MemoryPersistence persistence = new MemoryPersistence();
            MqttClient client = new MqttClient(broker, clientId, persistence);
            MqttConnectOptions options = new MqttConnectOptions();
            options.setCleanSession(true);
            options.setAutomaticReconnect(true);
            options.setConnectionTimeout(10);
            
            // Connect to broker
            System.out.println("Connecting to broker: " + broker);
            client.connect(options);
            System.out.println("Connected to broker");
            
            // Subscribe to feedback topic
            final String topicToSubscribe = subTopic;  // Need final var for lambda
            client.subscribe(topicToSubscribe, (topic, message) -> {
                String payload = new String(message.getPayload());
                System.out.println("Received message on " + topic + ": " + payload);
                if (payload.equals("stop")) {
                    System.out.println("Stop command received. Shutting down...");
                    running = false;
                }
            });
            System.out.println("Subscribed to topic: " + subTopic);
            
            // Publish sinus values
            double counter = 0.0;
            final String topicToPublish = pubTopic;  // Need final var for lambda
            while (running) {
                double sinusValue = Math.sin(counter);
                String payload = String.format("%.6f", sinusValue);
                
                MqttMessage message = new MqttMessage(payload.getBytes());
                message.setQos(0);
                
                client.publish(topicToPublish, message);
                System.out.println("Published message to " + topicToPublish + ": " + payload);
                
                counter += 0.1;
                Thread.sleep(1000);
            }
            
            // Disconnect
            client.disconnect();
            System.out.println("Disconnected from broker");
            
        } catch (MqttException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}