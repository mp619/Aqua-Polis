import datetime
import json
from dateutil.tz import tzutc
import smbus2
import time
import paho.mqtt.client as mqtt

client = mqtt.Client()
#client.tls_set(ca_certs="mosquitto.org.crt",certfile="client.crt",keyfile="client.key")
client.connect("broker.mqttdashboard.com",port=1883)

def Json_create( SensorReading ):
    a_datetime = datetime.datetime.now()
    time_stamp = a_datetime.isoformat()
    Reading_dic = {
        'TimeStamp': time_stamp,
        'SensorReading': SensorReading
    }
    json_output = json.dumps(Reading_dic)
    return json_output

bus = smbus2.SMBus(1)
temp_array = []

while True :
    
    #State address of ADC
    ADC_adr = 0x48
    #ADC useful register pointers - Comparator registers not required
    ADC_REG_PTR_Conv = 0x00 #Pointer to conversion register - note 16bits
    ADC_REG_PTR_Conf = 0x01 #Pointer to Config register - note 16bits

    #Configure ADC
    ADC_Reg_Gain = 0x02 # A gain of 1, hence a v_ref of around 3V

    #Write to Config Register for single-shot conversion
    Config_reg = smbus2.i2c_msg.write(ADC_adr,[ADC_REG_PTR_Conf,0xC2,0x83])
    Pointer_reg = smbus2.i2c_msg.write(ADC_adr,[ADC_REG_PTR_Conv])
    bus.i2c_rdwr(Config_reg)
    bus.i2c_rdwr(Pointer_reg)
    #wait for measurement
    time.sleep(0.1)
    #send the read ADC command and read two bytes of data
    Read_Conv = smbus2.i2c_msg.read(ADC_adr,2)
    bus.i2c_rdwr(Read_Conv)
    #convert the result to an int and turn negative numbers to 0
    temp = int.from_bytes(Read_Conv.buf[0]+Read_Conv.buf[1],"big")
    if temp > 32767:
	    temp = temp - 65535
    temp = temp*0.125	# Convert to mv
    temp = temp*0.001   # Convert to V
    #print binary values
    time.sleep(0.1)
    print(temp)
    temp_array.append(temp)
	
    if len(temp_array)== 5:
        json_output = Json_create( temp_array)
        temp_array = []
        print(json_output)
        MSG_INFO= client.publish("IC.embedded/M2S2/test",json_output)
        print(mqtt.error_string(MSG_INFO.rc))
