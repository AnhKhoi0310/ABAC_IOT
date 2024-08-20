import paho.mqtt.publish as publish

mqtt_broker_address = "172.16.58.123"

mqtt_channel = "your/command/channel"

msg = "Hello, from Raspberrypi II !"
try:
    publish.single(mqtt_channel, msg, hostname = mqtt_broker_address )
    print("Message sent successfully")
except Exception as e:
    print(f"Failed to send message: {e}")