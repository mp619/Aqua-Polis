import datetime
import ssl
import rsa
import json
from dateutil.tz import tzutc
import time
import paho.mqtt.client as mqtt

client = mqtt.Client()
# client.tls_set("ca.crt")
#client.tls_insecure_set(True)
# client.tls_set(ca_certs="ca-root-cert.crt", cert_reqs=ssl.CERT_NONE)
# client.tls_set(ca_certs='ca.crt', certfile='client.crt', keyfile='client.key', cert_reqs=ssl.CERT_NONE)
#client.tls_set(ca_certs="ca-root-cert.crt", cert_reqs=ssl.CERT_NONE)
# client.tls_set('ca.crt','client.crt','client.key')
client.connect("146.169.199.233",port=1883)

def Json_create( data ):
    a_datetime = datetime.datetime.now()
    time_stamp = a_datetime.isoformat()
    Reading_dic = {
        'TimeStamp': time_stamp,
        'Message': data
    }

    json_output = json.dumps(Reading_dic)
    return json_output



# prv_file = open ("private.pem", "w")
# pub_file = open ("public.pem", "w")
with open('private_pem', mode='rb') as privatefile:
    keydata = privatefile.read()
publicKey = rsa.PublicKey.load_pkcs1(keydata)

print(publicKey)
 

data = "hello salman"

json_output = Json_create( data)
print(json_output)

# rsa.encrypt method is used to encrypt
# string with public key string should be
# encode to byte string before encryption
# with encode method
encMessage = rsa.encrypt(json_output.encode(),
                         publicKey)
 
print("original string: ", encMessage)
print("encrypted string: ", encMessage)
MSG_INFO= client.publish("broker_try/Salman",encMessage)
print(mqtt.error_string(MSG_INFO.rc))


