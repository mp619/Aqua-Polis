import datetime
import json
from dateutil.tz import tzutc
import smbus2
import time
import paho.mqtt.client as mqtt

def on_message(client, userdata, message) :
    print("Received message:{} on topic{}".format(message.payload, message.topic))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(""IC.embedded/M2S2/#")

client = mqtt.Client()
client.tls_set(ca_certs="mosquitto.org.crt",certfile="client.crt",keyfile="client.key")
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org",port=1883)

def Json_create( SensorReading ):
    a_datetime = datetime.datetime.now()
    time_stamp = a_datetime.isoformat()
    Reading_dic = {
        'TimeStamp': time_stamp,
        'SensorReading': SensorReading
    }
    json_output = json.dumps(Reading_dic)
    return json_output

temp = []

# while True :
#     bus = smbus2.SMBus(1)
#     #send the measure temperature command
#     meas_temp= smbus2.i2c_msg.write(24,[0xAA,0x00,0x00])
#     bus.i2c_rdwr(meas_temp)
#     #wait for measurement
#     time.sleep(0.1)
#     #send the read temperature command and read two bytes of data
#     read_result= smbus2.i2c_msg.read(24,4)
#     bus.i2c_rdwr(read_result)
#     #convert the result to an int
#     temp.append(int.from_bytes(read_result.buf[0]+read_result.buf[1]+read_result.buf[2]+read_result.buf[3], "big"))
#     time.sleep(0.1)
#     print(temp)
#     if len(temp)== 5:
#         json_output = Json_create( temp)
#         temp = []
#         print(json_output)
#         MSG_INFO= client.publish("IC.embedded/M2S2/test",json_output)
#         print(mqtt.error_string(MSG_INFO.rc))

client.loop()