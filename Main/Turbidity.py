import smbus2
import time

#ADC useful register pointers - Comparator registers not required
ADC_REG_PTR_Conv = 0x00 #Pointer to conversion register - note 16bits
ADC_REG_PTR_Conf = 0x01 #Pointer to Config register - note 16bits 

def init():
    bus = smbus2.SMBus(1)
    return bus

def config(bus, ADC_adr):
    Config_reg = smbus2.i2c_msg.write(ADC_adr,[ADC_REG_PTR_Conf,0xD1,0x83])
    bus.i2c_rdwr(Config_reg)

def read(bus, ADC_adr):
    Pointer_reg = smbus2.i2c_msg.write(ADC_adr,[ADC_REG_PTR_Conv])
    bus.i2c_rdwr(Pointer_reg)
    #wait for measurement
    time.sleep(0.01)
    #send the read ADC command and read two bytes of data
    Read_Conv = smbus2.i2c_msg.read(ADC_adr,2)
    bus.i2c_rdwr(Read_Conv)
    #convert the result to an int and turn negative numbers to 0
    ADC_Value = int.from_bytes(Read_Conv.buf[0]+Read_Conv.buf[1],"big")
    return ADC_Value

def convert(adc):
    if adc > 32767:
	    adc = adc - 65535
    volts = adc*0.1875	# Convert to mv
    volts = volts*0.001   # Convert to V
    turb = (-1120.4*pow(volts,2) + 5742.3*volts - 4352.9)
    #turb = (-1250*volts + 4999.25)*0.001 #Convert Voltage to NTUs
    if turb < 0:
        turb = 0
    return turb