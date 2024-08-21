import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from cryptography.hazmat.primitives import serialization
import json
import time
import base64
import io
import os
from PIL import Image
from compare_images import compare_images
from ECC.decrypt import decrypt_message
from interfaces.accessControl import access_control
from interfaces.updateTrustPoint import update_point
# Define the MQTT settings
MQTT_BROKER = "localhost"  # or broker's IP address
MQTT_PORT = 1883
MQTT_RECEIVE_REQUEST = "request/permit" # to receive request from lock
MQTT_REQUEST_IMAGE = "request/image" # to send image request to camera
MQTT_SEND_IMAGE = "send/image" # to receive normal image from camera
MQTT_PERMISSION = "send/permit" # To send permission to the lock
MQTT_RECEIVE_KEY = "exchange/key" # To receive key from camera, for initial setup
MQTT_RECEIVE_MESSAGE = "exchange/message" # To reveive text message from camera, for testing
MQTT_RECEIVE_IMAGE = "exchange/image" # to receive decrypted image from camera
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_RECEIVE_REQUEST)
    client.subscribe(MQTT_SEND_IMAGE)
    client.subscribe(MQTT_RECEIVE_KEY)
    client.subscribe(MQTT_RECEIVE_MESSAGE)
    client.subscribe(MQTT_RECEIVE_IMAGE)

def start_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

def on_message(client, userdata, msg):
    # print(f"Received message {msg.topic}: {json.loads(msg.payload.decode())}")
    if msg.topic == MQTT_RECEIVE_REQUEST:
        global first_message_time
        # Get the current time for recording purpose
        first_message_time = time.time()
        # check the policies
        start = time.time()
        data = json.loads(msg.payload.decode())
        SubjectAddress = data['SubjectAddress']
        ObjectAddress = data['ObjectAddress']
        permission = access_control(SubjectAddress, ObjectAddress)
        print("Permission:",permission)
        if(permission == True):
            try:
                client.publish(MQTT_REQUEST_IMAGE, json.dumps(data))
                print("Send request image successfully!")
            except Exception as e:
                print("Unable to send image request: ", e)
        else:
            permission = False
            client.publish(MQTT_PERMISSION, json.dumps({"permission": permission}))
            print("Send DENIAL permission successfully!") 
        end = time.time()
        print("The time of execution of Blockchain access control program is :", (end-start) * 10**3, "ms")
    elif msg.topic == MQTT_SEND_IMAGE: # to receive normal image from camera
        try:
            base64_image_string = msg.payload.decode('utf-8')
            missing_padding = len(base64_image_string) % 4
            if missing_padding != 0:
                base64_image_string += '=' * (4 - missing_padding)
            image_data = base64.b64decode(base64_image_string) # in string
            image = Image.open(io.BytesIO(image_data))
            image = image.convert('RGB')
            # Save the image to a file
            image.save("images/person.jpg")
            print(f"Image saved successfully to {os.getcwd()}/images/person.jpg")
            #  compare the image from camera with existing images from database
            permission = compare_images()
            client.publish(MQTT_PERMISSION, json.dumps(permission))
            print("Send permission successfully!")          
        except Exception as e:
            print(f"Failed to decode and save normal image: {e}") 
    elif msg.topic == MQTT_RECEIVE_KEY: # to receive key from camera
        data = json.loads(msg.payload.decode())
        encoded_public_key = data["public_key"]
        print(encoded_public_key)
        try:
            with open("config.json", 'r') as file:
                data = json.load(file) 
                data['public_key'] = encoded_public_key           
            with open("config.json", 'w') as file:
                json.dump(data, file, indent=4)
            print("Saving public Key successfully!")
        except Exception as e:
            print("Error saving public key ",e)
    elif msg.topic == MQTT_RECEIVE_MESSAGE: # to receive text message from camera/lock
        data = json.loads(msg.payload.decode())
        try: 
            encoded_iv = data["encoded_iv"]
            encoded_ciphertext = data["encoded_ciphertext"]
            encoded_tag = data["encoded_tag"]
            # Decode the json and convert back to object
            iv = base64.b64decode(encoded_iv)
            ciphertext = base64.b64decode(encoded_ciphertext)
            tag = base64.b64decode(encoded_tag)  
            # Decrypt the message      
            print(decrypt_message(iv,ciphertext,tag))
        except Exception as e:
            print("Error decrypting message:", e)
        # HANDLE DECRYPTED IMAGE
    elif msg.topic == MQTT_RECEIVE_IMAGE: # to receive encrypted image from camera
        data = json.loads(msg.payload.decode())
        try:
            start = time.time() 
            SubjectAddress = data['SubjectAddress']
            encoded_iv = data["encoded_iv"]
            encoded_image = data["encoded_ciphertext"]
            encoded_tag = data["encoded_tag"]
            # Decode the json and convert back to object
            iv = base64.b64decode(encoded_iv)
            cipher_image = base64.b64decode(encoded_image)
            tag = base64.b64decode(encoded_tag)  
            # Decrypt the message      
            image_data = decrypt_message(iv,cipher_image,tag)
            end = time.time()        
            print("The time of execution for image decryption is :", (end-start) * 10**3, "ms")               
            image = Image.open(io.BytesIO(image_data))
            image = image.convert('RGB')
            # Save the image to a file
            image.save("images/person.jpg")
            print(f"Image saved successfully to {os.getcwd()}/images/person.jpg")
            #  compare the image from camera with existing images from database
            permission = compare_images()
            if permission == True:
                print("Send ACCEPTANCE permission successfully!") 
                client.publish(MQTT_PERMISSION, json.dumps({"permission":permission, "message": "Open the door!"}))         
            else: 
                print("Send DENIAL permission successfully!") 
                client.publish(MQTT_PERMISSION, json.dumps({"permission":permission, "message": "Doesn't have your face in database"}))
        except Exception as e:
            print(f"Failed to decode and save encrypted image: {e}") 
        
        start = time.time()
        try:
            update_status = update_point(SubjectAddress)
            print("Update Status:", update_status)
        except Exception as e:
            print(" Error when updating trust point, check calculateTrustPoint.py,  getPeaks.py, updateTrustPoint.py, getHistory.py:", e)    
        end = time.time()
        print("The time of execution for trust update is :", (end-start) * 10**3, "ms")
        end_entire_program = time.time()
        print("The time of execution for entire program is :", (end_entire_program- first_message_time) * 10**3, "ms")


if __name__ == "__main__":
    start_client()


