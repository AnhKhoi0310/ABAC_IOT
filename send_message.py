#This file is use for initial setup/ testing image communication
import paho.mqtt.publish as publish
import json
import base64
mqtt_broker_address = "172.16.58.26"  # Use the same broker as receiver
from ECC.encrypt import encrypt_message
mqtt_channel = "exchange/message"
message = "Hello Khoi"
try:
    iv, ciphertext, tag = encrypt_message(message)
    encoded_iv = base64.b64encode(iv).decode('utf-8')
    encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    encoded_tag = base64.b64encode(tag).decode('utf-8')
    # print(iv)
    # print(ciphertext)
    # print(tag)
except Exception as e:
    print(e)

msg = {
        'encoded_iv': encoded_iv,
        'encoded_ciphertext' : encoded_ciphertext,
        "encoded_tag" :encoded_tag
    }

try:
    publish.single(mqtt_channel, json.dumps(msg), hostname=mqtt_broker_address)
    print("Public key sent successfully")
except Exception as e:
    print(f"Failed to send publick key: {e}")