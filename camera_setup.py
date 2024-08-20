import paho.mqtt.client as mqtt
import json
import base64
from PIL import Image
import io
from cryptography.hazmat.primitives import serialization
from capture import capture
from ECC.encrypt import encrypt_message
# from send_image import 

# Define the MQTT settings
MQTT_BROKER = "172.16.58.38"  #  broker's IP address
MQTT_PORT = 1884
MQTT_RECEIVE_REQUEST = "request/image"
MQTT_SEND_IMAGE = "send/image"
MQTT_RECEIVE_KEY = "exchange/key" # To receive key from server, for initial setup
MQTT_SEND_ENCRYPTED_IMAGE = "exchange/image" # To send encrypted image to server

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_RECEIVE_REQUEST)
    client.subscribe(MQTT_RECEIVE_KEY)

def start_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(f"Received message: {data}")
    if msg.topic == MQTT_RECEIVE_REQUEST:
        # Send Normal/Unencrypted Image
        # capture()
        # try:
        #     with open("test.jpg", "rb") as image_file:
        #         image_data = image_file.read()
        #         encoded_image = base64.b64encode(image_data).decode('utf-8')        
        #     client.publish(MQTT_SEND_IMAGE, encoded_image)
        #     print("Send image from camera success!")
        # except Exception as e:
        #     print(f"Failed to send unencrypted image: {e}")
        
        # Send Normal/Unencrypted Image
        try:
            SubjectAddress = data['SubjectAddress']
            with open("A20.jpg", "rb") as image_file:
                image_data = image_file.read()
            iv, ciphertext, tag = encrypt_message(image_data)
            encoded_iv = base64.b64encode(iv).decode('utf-8')
            encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
            encoded_tag = base64.b64encode(tag).decode('utf-8')
            msg = {
                'SubjectAddress': SubjectAddress,
                'encoded_iv': encoded_iv,
                'encoded_ciphertext' : encoded_ciphertext,
                "encoded_tag" :encoded_tag
            }
            client.publish(MQTT_SEND_ENCRYPTED_IMAGE, json.dumps(msg))
            print(" Decripted image sent successfully")
        except Exception as e:
            print(f"Failed to send decrypted image key: {e}")
    elif msg.topic == MQTT_RECEIVE_KEY:
        data = json.loads(msg.payload.decode())
        encoded_public_key = data["public_key"]
        print(encoded_public_key)
        try:
            with open("config.json", 'r') as file:
                data = json.load(file) 
                data['public_key'] = encoded_public_key   # in based64 (with header & footer) json string
            with open("config.json", 'w') as file:
                json.dump(data, file, indent=4)
            print("Saving public Key success!")
        except Exception as e:
            print("Error saving public key ",e)

if __name__ == "__main__":
    start_client()
