from threading import Thread
import time
import smbus2
import TDS as TDS
import Turbidity as Turb
import RGB
import paho.mqtt.client as mqtt
import datetime
import json
from dateutil.tz import tzutc
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

key_file = open("rprivate-key.pem", "rb")
private_key = serialization.load_pem_private_key(
    key_file.read(),
    password=None,
    backend=default_backend()
)

key_file = open("public-key.pem", "rb")
public_key = serialization.load_pem_public_key(
    key_file.read(),
    backend=default_backend()
)

#Global Variable for LED Thread
STATUS = 1

def on_connect(client, userdata, flags, rc):
    global STATUS
    print(rc)
    if rc ==0:
        print("Successful Connection")
        #print("Connected with result code "+str(rc))
        client.subscribe("IC.embedded/M2S2/#")
        STATUS = 6
    else:
        print("Bad Connection, returned code=", rc)
        STATUS = 7


def on_message(client, userdata, message) :
    global STATUS
    print("Received message:{} on topic{}".format(message.payload, message.topic))
    if(message.topic=="IC.embedded/M2S2/results"):
        original_message = private_key.decrypt(message.payload,
                                                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                            algorithm=hashes.SHA256(),
                                                            label=None
                                                            )
                                                )
        # decode and turn from json to dict 
        data = str(original_message.decode())
        drink = data.split()[0]
        print(drink)
        if drink == 'True':
            STATUS = 2
        else:
            STATUS = 3
#        client.loop_stop()

#MQTT
client = mqtt.Client()
#client.tls_set(ca_certs="mosquitto.org.crt",certfile="client.crt",keyfile="client.key")
try :
    client.connect("146.169.199.233",port=1883)
    STATUS = 6
except:
    STATUS = 7
#client.on_connect = on_connect
client.subscribe("IC.embedded/M2S2/#")
client.on_message = on_message
client.on_publish = print('Published readings to broker')
client.on_subscribe = print('Subscribed to all topics')

#temp_array = []

# Init Objects
bus = smbus2.SMBus(1)
led = RGB.RGBInit()
button = RGB.ButtonInit()

#TDS Config
ADC_adr = 0x48 # ADC I2C address

# 1 Turns off LED
# 2 Clean - Green
# 3 Dirty - Red
# 4 Processing - Blue flashing
# 5 Sending/Receiving - Yellow
# 6 Before Button Press - Blue
# 7 Comms Failed - Red Flashing

def ledcolor():
    global STATUS
    while STATUS:
        if STATUS == 1:
            RGB.StatusOff(led)
        elif STATUS == 2:
            RGB.StatusClean(led)
        elif STATUS == 3:
            RGB.StatusDirty(led)
        elif STATUS == 4:
            RGB.StatusMeasuring(led)
        elif STATUS == 5:
            RGB.StatusSending(led)
        elif STATUS == 6:
            RGB.StatusOn(led)
        elif STATUS == 7:
            RGB.StatusFailSending(led)
        else:
            break

def Json_create( TDS_value, Turb_Value, Lon, Lat ):
    a_datetime = datetime.datetime.now()
    time_stamp = a_datetime.isoformat()
    Reading_dic = {
        'TimeStamp': time_stamp,
        'TDS': TDS_value,
        'TSS': Turb_Value,
        'Lon': Lon,
        'Lat': Lat
    }
    json_output = json.dumps(Reading_dic)
    return json_output

LED_Thread = Thread(target=ledcolor)
LED_Thread.start()
#Message_Thread = Thread(target=client.loop_forever())
#Message_Thread.start()

while True:
    client.reconnect()
    if RGB.Press(button):
        print('Button Pressed...')
        ## Get TDS and Turb value
        STATUS = 4  # Processing 
        TDS_Total = 0
        Turb_Total = 0
        cycles = 100

        ## Get TDS value
        for i in range(1,cycles):
            TDS.config(bus, ADC_adr)
            time.sleep(0.01)
            TDS_Total = TDS_Total + TDS.read(bus, ADC_adr)
        TDS_adc = TDS_Total/cycles
        TDS_value = TDS.convert(TDS_adc)

        ## Get Turb value
        for i in range(1,cycles):
            Turb.config(bus, ADC_adr)
            time.sleep(0.01)
            Turb_Total = Turb_Total + Turb.read(bus, ADC_adr)
        Turb_adc = Turb_Total/cycles
        print(Turb_adc)
        Turb_value = Turb.convert(Turb_adc)

        print(TDS_value, 'ppm')
        print(Turb_value, 'NTU')

        ## Get Long and Lat to seen
        try:
            url = 'https://extreme-ip-lookup.com/json/'
            r = requests.get(url)
            data = json.loads(r.content.decode())
            ip = data['query']
            response = requests.get("https://geolocation-db.com/json/"+ip+"&position=true").json()
            lat = response['latitude']
            lon = response['longitude']
            print("Latitude: ", lat)
            print("Longitude: ", lon)
        except:
            # ideally a GPS module would be used to collect location data
            lat = 51.4963
            lon = -0.1769

        ## Send to broker
        STATUS = 5
        json_output = Json_create( TDS_value, Turb_value, lat, lon)
        print(json_output)
        json_output = json_output.encode()
        encMessage = public_key.encrypt(json_output,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        MSG_INFO= client.publish("IC.embedded/M2S2/readings",json_output)
        print(mqtt.error_string(MSG_INFO.rc))
        client.loop_start()

