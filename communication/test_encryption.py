from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


key_file = open("private-key.pem", "rb") 
private_key = serialization.load_pem_private_key(key_file.read(),password=None,backend=default_backend())
key_file = open("public-key.pem", "rb")
public_key = serialization.load_pem_public_key(key_file.read(),backend=default_backend())
message = b'Hello Mati'
encrypted = public_key.encrypt(message,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
original_message = private_key.decrypt(encrypted,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
print(encrypted)
print(original_message)
