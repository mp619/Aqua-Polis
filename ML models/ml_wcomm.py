import paho.mqtt.client as mqtt
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
import sklearn 
from joblib import dump, load
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Load private and public keys for encryption

key_file = open("rasp_comm/private-key.pem", "rb") 
private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

key_file = open("rasp_comm/public-key.pem", "rb")
public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

# load models into variables to be used for prediction

rf1 = load('/Users/salmandhaif/Desktop/Year3/ES/models/forest1') 
rf2 = load('/Users/salmandhaif/Desktop/Year3/ES/models/forest4') 
rf3 = load('/Users/salmandhaif/Desktop/Year3/ES/models/forest3') 
rf4 = load('/Users/salmandhaif/Desktop/Year3/ES/models/forest4') 

# define on message callback 
# listen to see if values published by sensors on /readings
# if so, decrypt, 
def on_message(client, userdata, message):
    print("Received message:{} on topic{}".format(message.payload, message.topic))
    if(message.topic=="IC.embedded/M2S2/readings"):
        # decode and turn from json to dict
        print()
        print(message.payload)
        print()
        original_message = private_key.decrypt(message.payload,
                                               padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                            algorithm=hashes.SHA256(),
                                                            label=None
                                                            )               
                                            )
        print(original_message.decode())
        data = json.loads(original_message.decode())

        # store necessary vars into containers
        tds = data['TDS']
        tss = data['TSS']

        # predict using each model then take majority vote 
        into_dt = np.array([tds,tss]).reshape(1,2)
        y_pred1 = rf1.predict(into_dt)
        y_pred2 = rf2.predict(into_dt)
        y_pred1g = rf3.predict(into_dt)
        y_pred2g = rf4.predict(into_dt)

        y_pp = y_pred1+y_pred2+y_pred1g+y_pred2g
        # would rather predict false negatives than false positives
        if y_pp > 2:
            data['drink'] = True
        else:
            data['drink'] = False

        # frame data for sending
        tbs = str(data['drink'])+' '+str(float("{:.3f}".format(data['TDS'])))+' '+str(float("{:.3f}".format(data['TSS'])))+' '+str(data['Lon'])+' '+str(data['Lat'])+' '+str(data['TimeStamp'])

        # encrypt message again        
        encrypted = public_key.encrypt(
            tbs.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        MSG_INFO= client.publish("IC.embedded/M2S2/results",(encrypted),2)
        print(mqtt.error_string(MSG_INFO.rc))



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("IC.embedded/M2S2/#")

broker_ip = "146.169.192.214"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip,port=1883)

client.loop_forever()

        