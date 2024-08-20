import paho.mqtt.publish as publish
import json
from cryptography.hazmat.primitives.asymmetric import ec # Provides elliptic curve cryptography primitives.
from cryptography.hazmat.primitives.kdf.hkdf import HKDF #Key derivation function used to derive a key from the shared secret.
from cryptography.hazmat.primitives import hashes #Provides hashing algorithms used in HKDF.
from cryptography.hazmat.primitives import serialization
import base64
mqtt_broker_address = "172.16.58.87"  # Use the same broker as receiver
# PEM format = Base64-encoded data wrapped in headers and footers: used to encode cryptographic keys and certificates
# Base64 Encoding: Typically used to convert binary data to an ASCII string for safe transmission or storage.

mqtt_channel = "exchange/key"
private_key = ec.generate_private_key(ec.SECP256R1())
# save the private key to the json file
try:
    # Serialize private key to byte format using PEM encoding
    private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM, #returns the PEM-encoded public key including the headers and footers.
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption() # to say that no encryption is used for security
    )
    with open("config.json", 'r') as file:
        data = json.load(file) 
        # converting the serialized private key from bytes to a string format that can be stored in a JSON file.
        # data['private_key'] = private_key_bytes.decode('utf-8') #Converting PEM Bytes to String
        data['private_key'] = base64.b64encode(private_key_bytes).decode('utf-8')  #Base64 Encoding Again to a single continuous base64 string. -- UTF-8 Decoding: Converts bytes to a string.
    with open("config.json", 'w') as file:
        json.dump(data, file, indent=4)
except Exception as e:
    print("Error saving key ",e)
# Create public key accoring to the private key
public_key = private_key.public_key()
print("public key:", public_key)

# Serialize public key to Byte format
pem_public_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM, #returns the PEM-encoded public key including the headers and footers.
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Encode PEM Byte format public key to base64-encoded string then to UTF-8 string to make it JSON serializable
encoded_public_key = base64.b64encode(pem_public_key).decode('utf-8') #Base64 Encoding Again to a single continuous base64 string --UTF-8 Decoding: Converts bytes to a string.
print("encoded_public_key: ", encoded_public_key)

msg = {
        'public_key': encoded_public_key,
    }
try:
    publish.single(mqtt_channel, json.dumps(msg), hostname=mqtt_broker_address)
    print("Public key sent successfully")
except Exception as e:
    print(f"Failed to send publick key: {e}")