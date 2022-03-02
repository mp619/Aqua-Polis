import datetime
import ssl
# import rsa
import json
from dateutil.tz import tzutc
import time
import paho.mqtt.client as mqtt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

client = mqtt.Client()
# client.tls_set("ca.crt")
#client.tls_insecure_set(True)
# client.tls_set(ca_certs="ca-root-cert.crt", cert_reqs=ssl.CERT_NONE)
# client.tls_set(ca_certs='ca.crt', certfile='client.crt', keyfile='client.key', cert_reqs=ssl.CERT_NONE)
#client.tls_set(ca_certs="ca-root-cert.crt", cert_reqs=ssl.CERT_NONE)
# client.tls_set('ca.crt','client.crt','client.key')
client.connect("146.169.192.214",port=8883)

def Json_create():
    a_datetime = datetime.datetime.now()
    time_stamp = a_datetime.isoformat()
    Reading_dic = {'TimeStamp': '2022-03-02T12:33:21.741011', 'TDS': 1299.3465038646998, 'TSS': 3.001571460745775, 'Lon': 51.4963, 'Lat': -0.1769}



    json_output = json.dumps(Reading_dic)
    return json_output



# prv_file = open ("private.pem", "w")
# pub_file = open ("public.pem", "w")
# with open('private_pem', mode='rb') as privatefile:
#     keydata = privatefile.read()
# publicKey = rsa.PublicKey.load_pkcs1(keydata)

# print(publicKey)
 

data = "hello salman"

json_output = Json_create()
print(json_output)

key_file = open("private-key.pem", "rb") 
private_key = serialization.load_pem_private_key(key_file.read(),password=None,backend=default_backend())
key_file = open("public-key.pem", "rb")
public_key = serialization.load_pem_public_key(key_file.read(),backend=default_backend())
json_output = json_output.encode()
encMessage = public_key.encrypt(json_output,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
# encMessage = rsa.encrypt(json_output.encode(),
                        #  publicKey)
 
print("original string: ", encMessage)
print("encrypted string: ", encMessage)
MSG_INFO= client.publish("IC.embedded/M2S2/readings",encMessage)
print(mqtt.error_string(MSG_INFO.rc))


