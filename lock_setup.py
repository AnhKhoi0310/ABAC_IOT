import paho.mqtt.client as mqtt_client
import json
mqtt_broker_address = "172.16.58.64"
MQTT_RECEIVE_PERMIT = "send/permit"
MQTT_PORT = 1883
# Callback function when a message is received
def on_message(client, userdata, msg):
    print(f"Received message: {(msg.payload.decode())}")
# Callback function when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    if rc == 0:
        client.subscribe(MQTT_RECEIVE_PERMIT)
        print(f"Subscribed to topic {MQTT_RECEIVE_PERMIT}")
    else:
        print(f"Failed to connect, return code {rc}")

# Create MQTT client and set callback functions
client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message

# Enable logging
client.enable_logger()

# Connect to the broker
client.connect(mqtt_broker_address, MQTT_PORT)

# Start the loop to process received messages
client.loop_start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()
