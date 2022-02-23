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

#MQTT
client = mqtt.Client()
#client.tls_set(ca_certs="mosquitto.org.crt",certfile="client.crt",keyfile="client.key")
client.connect("broker.mqttdashboard.com",port=1883)
temp_array = []

# Init Objects
bus = smbus2.SMBus(1)
led = RGB.RGBInit()
button = RGB.ButtonInit()

#TDS Config
ADC_adr = 0x48 # ADC I2C address
TDS.config(bus, ADC_adr)

#Turb Config
Turb.config(bus, ADC_adr)

#Global Variable for LED Thread
STATUS = 0
# 0 Turns off thread
# 1 Clean - Green
# 2 Dirty - Red
# 3 Processing - Yellow
# 4 Sending/Receiving - Yellow Flashing

def ledcolor():
    global STATUS
    while STATUS:
        if STATUS == 0:
            RGB.StatusOff()
        elif STATUS == 1:
            RGB.StatusClean(led)
        elif STATUS == 2:
            RGB.StatusDirty(led)
        elif STATUS == 3:
            RGB.StatusMeasuring(led)
        elif STATUS == 4:
            RGB.StatusSending(led)
        else:
            break

def Json_create( TDS_Value, Turb_Value ):
    a_datetime = datetime.datetime.now()
    time_stamp = a_datetime.isoformat()
    Reading_dic = {
        'TimeStamp': time_stamp,
        'TDS': TDS_value,
        'TSS': Turb_Value
    }
    json_output = json.dumps(Reading_dic)
    return json_output


LED_Thread = Thread(target=ledcolor)
LED_Thread.start()

while True:
    if RGB.Press(button):
        ## Get TDS and Turb value
        STATUS = 3  # Processing 
        TDS_Total = 0
        Turb_Total = 0
        cycles = 100
        for i in range(1,cycles):
            TDS_Total = TDS_Total + TDS.read(bus, ADC_adr)
            Turb_Total = Turb_Total + Turb.read(bus, ADC_adr)
            print(TDS_Total)
        TDS_adc = TDS_Total/cycles
        Turb_adc = Turb_Total/cycles
        TDS_value = TDS.convert(TDS_adc)
        print(TDS_value)
        Turb_value = Turb.convert(Turb_adc)
        print(Turb_value)

        ## Send to broker
        json_output = Json_create( TDS_value, Turb_value)
        print(json_output)
        MSG_INFO= client.publish("IC.embedded/M2S2/test",json_output)
        print(mqtt.error_string(MSG_INFO.rc))

