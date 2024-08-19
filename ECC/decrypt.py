from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
import os
import json
import base64
from cryptography.hazmat.primitives import serialization
file_path = "config.json"
def decrypt_message(iv,  ciphertext, tag):
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
        # Resolve the shared secret 
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
    decryptor = Cipher(
        algorithms.AES(derived_key),
        modes.GCM(iv, tag),
    ).decryptor()
    
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext
# decrypt_message(b"2SU+FXthw+nR6Lrl", b"J4OWesuu8KZrNw==",b"3dqhU8C/kSLjW2GIZTD6dQ==")