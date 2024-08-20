import paho.mqtt.client as mqtt_client
import random
import base64
import io
import os
from PIL import Image
client_id = f'python-mqtt-{random.randint(0, 1000)}'
mqtt_broker_address = "172.16.58.123"
mqtt_channel = "your/image/channel"

# Callback function when a message is received
def on_message(client, userdata, message):
    print("on_message callback invoked")
    try:
        print(f"Message received on topic {message.topic}")
        # Decode the base64 string to bytes
        base64_image_string = message.payload.decode('utf-8')
        print("Base64 string decoded")

        # Add padding if necessary to make the length a multiple of 4
        missing_padding = len(base64_image_string) % 4
        if missing_padding != 0:
            base64_image_string += '=' * (4 - missing_padding)
        print("Padding added if necessary")

        # Decode base64 string to bytes
        image_data = base64.b64decode(base64_image_string)
        print("Base64 string decoded to bytes")

        # Convert bytes to image
        image = Image.open(io.BytesIO(image_data))
        print("Bytes converted to image")

        # Convert the image to RGB mode (or RGBA if it has an alpha channel)
        image = image.convert('RGB')
        print("Image converted to RGB mode")

        # Save the image to a file
        image.save("decoded_image.jpg")
        print(f"Image saved successfully to {os.getcwd()}/decoded_image.jpg")
    except Exception as e:
        print(f"Failed to decode and save image: {e}")

# Callback function when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    if rc == 0:
        client.subscribe(mqtt_channel)
        print(f"Subscribed to topic {mqtt_channel}")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback function when the client subscribes to a topic
def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscribed to topic with QoS {granted_qos}")

# Create MQTT client and set callback functions
client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

# Enable logging
client.enable_logger()

# Connect to the broker
client.connect(mqtt_broker_address)

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
