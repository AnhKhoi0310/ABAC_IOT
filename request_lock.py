import paho.mqtt.publish as publish
import json
from datetime import datetime 
mqtt_broker_address = "172.16.58.40"  # Use the same broker as receiver

mqtt_channel = "request/permit"

# msg = {
#         'type': 'lock',
#         'time':  str(datetime.now().time()),
#         'requested_device': 'camera',
#         'request_image': True
#     }
msg = {
        'SubjectAddress': '0xe8D12D6e500A614fe06b4268Cbda0e751E8682Cd',
        'ObjectAddress': '0xcD1BcDdaCe60a995cF54ffD4Df39087c9Bb950d1',
    }
try:
    publish.single(mqtt_channel, json.dumps(msg), hostname=mqtt_broker_address)
    print("Message sent successfully")
except Exception as e:
    print(f"Failed to send message: {e}")