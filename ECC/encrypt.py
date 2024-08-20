from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
import os
import json
import base64
from cryptography.hazmat.primitives import serialization
def encrypt_message( message):
    file_path = "config.json"
    # check if the message is already in bytes type
    if not isinstance(message, bytes):
        message = message.encode('utf-8')
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as file:
            data = json.load(file) 
        # get the encode_public_key and convert it to public_key
        encoded_public_key = data['public_key']        
        pem_public_key = base64.b64decode(encoded_public_key) #In Byte-format (PEM decoding), done directly without additional UTF-8 decoding.
        public_key = serialization.load_pem_public_key(pem_public_key)# public key -- reads the PEM format, recognizes the headers and footers, and reconstructs the key object
        # get the encode_public_key and convert it to public_key
        encoded_private_key = data['private_key']
        pem_private_key = base64.b64decode(encoded_private_key)
        private_key = serialization.load_pem_private_key(
            pem_private_key,
            password=None,  
        )       
        shared_secret = private_key.exchange(ec.ECDH(), public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_secret)
    else:
        print(f"Json file does not exist or is empty")
        return False
    iv = os.urandom(12)  # Generate a random 12-byte IV
    encryptor = Cipher(
        algorithms.AES(derived_key),
        modes.GCM(iv),
    ).encryptor()
    
    ciphertext = encryptor.update(message) + encryptor.finalize()
    return iv, ciphertext, encryptor.tag


# message = "Hello, IoT World!"
# iv, ciphertext, tag = encrypt_message(message)
# print("IV", iv)
# print("Encrypted message:", ciphertext)
# print("Tag:", tag)