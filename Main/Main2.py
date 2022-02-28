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

def on_connect(client, userdata, flags, rc):

    print("Connected with result code "+str(rc))
    client.subscribe("IC.embedded/M2S2/#")


def on_message(client, userdata, message) :
   print("Received message:{} on topic{}".format(message.payload, message.topic))
   if(message.topic=="IC.embedded/M2S2/results"):
   # decode and turn from json to dict 
       data = json.loads(message.payload)
       drink = data['drink']
       if drink == 'true':
           STATUS = 2
       else:
           STATUS = 3
       client.loop_stop()

#MQTT
client = mqtt.Client()
#client.tls_set(ca_certs="mosquitto.org.crt",certfile="client.crt",keyfile="client.key")
client.connect("146.169.198.107",port=1883)
client.on_connect = on_connect
client.on_message = on_message

#temp_array = []

# Init Objects
bus = smbus2.SMBus(1)
led = RGB.RGBInit()
button = RGB.ButtonInit()

#TDS Config
ADC_adr = 0x48 # ADC I2C address


#Turb Config
Turb.config(bus, ADC_adr)

#Global Variable for LED Thread
STATUS = 1
# 1 Turns off LED
# 2 Clean - Green
# 3 Dirty - Red
# 4 Processing - Yellow
# 5 Sending/Receiving - Yellow Flashing
# 6 Before Button Press - Blue

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
    STATUS = 6
    if not RGB.Press(button):
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
            lat = 51.4963
            lon = -0.1769

        ## Send to broker
        STATUS = 5
        json_output = Json_create( TDS_value, Turb_value, lat, lon)
        print(json_output)
        MSG_INFO= client.publish("IC.embedded/M2S2/sensor",json_output)
        print(mqtt.error_string(MSG_INFO.rc))
        client.loop_start()



