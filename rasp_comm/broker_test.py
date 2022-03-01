import datetime
import json
from dateutil.tz import tzutc
import time
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("146.169.195.84",port=1883)

def Json_create( data ):
    a_datetime = datetime.datetime.now()
    time_stamp = a_datetime.isoformat()
    Reading_dic = {
        'TimeStamp': time_stamp,
        'Message': data
    }

    json_output = json.dumps(Reading_dic)
    return json_output

data = "hello Salman"
json_output = Json_create( data)
print(json_output)
MSG_INFO= client.publish("broker_try/Salman",json_output)
print(mqtt.error_string(MSG_INFO.rc))
