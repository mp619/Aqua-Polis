import smbus2
import time

#get I2C bus
bus = smbus2.SMBus(1)

while True :
    #State address of ADC
    ADC_adr = 0x48
    #ADC useful register pointers - Comparator registers not required
    ADC_REG_PTR_Conv = 0x00 #Pointer to conversion register - note 16bits
    ADC_REG_PTR_Conf = 0x01 #Pointer to Config register - note 16bits

    #Configure ADC
    ADC_Reg_Gain = 0x02 # A gain of 1, hence a v_ref of around 3V
    #Write to Config Register for single-shot conversion
    total = 0    # Intialize total
    for i in range(0, 10):
        Config_reg = smbus2.i2c_msg.write(ADC_adr,[ADC_REG_PTR_Conf,0xD1,0x83])
        Pointer_reg = smbus2.i2c_msg.write(ADC_adr,[ADC_REG_PTR_Conv])
        bus.i2c_rdwr(Config_reg)
        bus.i2c_rdwr(Pointer_reg)
        #wait for measurement
        time.sleep(0.01)
        #send the read ADC command and read two bytes of data
        Read_Conv = smbus2.i2c_msg.read(ADC_adr,2)
        bus.i2c_rdwr(Read_Conv)
        #convert the result to an int and turn negative numbers to 0
        t1 = int.from_bytes(Read_Conv.buf[0]+Read_Conv.buf[1],"big")
        total = total + t1
    avg = total/10
    if avg > 32767:
	    avg = avg - 65535
    volts = avg*0.1875	# Convert to mv
    volts = volts*0.001   # Convert to V
    turb = (-1250*volts + 4999.25)*0.001 
    #print binary values
    time.sleep(0.1)
    #print(format(temp, "016b"))
    print(turb, "NTU")
