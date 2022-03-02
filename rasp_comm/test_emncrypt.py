import datetime
import ssl
import rsa
import json
from dateutil.tz import tzutc
import time
import paho.mqtt.client as mqtt


# with open('public_pem', mode='r') as publicfile:
#     keydata = publicfile.read()
# publicKey = rsa.PublicKey.load_pkcs1(keydata)
file1 = open('public_pem1', 'r')
key = file1.read()
publicKey = rsa.PublicKey.load_pkcs1(key)
file1.close()
print(publicKey)


# import rsa
# publicKey, privateKey = rsa.newkeys(1024)
# def encrypt(public_key, data):
#    return rsa.encrypt(data.encode(), public_key)
# def decrypt(private_key, data):
#     return rsa.decrypt(data, privateKey).decode()
# public_key_string = publicKey.save_pkcs1().decode("utf-8")
# private_key_string = privateKey.save_pkcs1().decode("utf-8")
# print(type(public_key_string))  # returns <class 'str'>
# print(type(private_key_string)) # returns <class 'str'>

# encrypted = encrypt(rsa.PublicKey.load_pkcs1(public_key_string), "Hello!")
# decrypted = decrypt(rsa.PublicKey.load_pkcs1(private_key_string), encrypted)
# print(decrypted)

# from Crypto.PublicKey import RSA

# key = RSA.generate(2048)
# f = open('mykey.pem','wb')
# f.write(key.export_key('PEM'))
# f.close()
# ...
# f = open('mykey.pem','r')
# key = RSA.import_key(f.read())
# # publicKey, privateKey = RSA.generate(1024)
# # privateKey.export_key('PEM')
# # publicKey.export_key(format='PEM')
# # public_pem = os.path.join('/keys', 'public.pem')
# # private_pem = os.path.join('/keys', 'private.pem')
# # with open(public_pem, 'x') as fp:
# #     fp.write(public_key.save_pkcs1().decode())
# # with open(private_pem, 'x') as fp:
# #     fp.write(private_key.save_pkcs1().decode())