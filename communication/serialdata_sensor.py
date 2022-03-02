import smbus2
import time

while true :
    bus = smbus2.SMBus(1)
    #send the measure temperature command
    meas_temp= smbus2.i2c_msg.write(24,[0xAA,0x00,0x00])
    bus.i2c_rdwr(meas_temp)
    #wait for measurement
    time.sleep(0.1)
    #send the read temperature command and read two bytes of data 
    read_result= smbus2.i2c_msg.read(24,4)
    bus.i2c_rdwr(read_result)
    #convert the result to an int
    temp = int.from_bytes(read_result.buf[0]+read_result.buf[1]+read_result.buf[2]+read_result.buf[3], "big")
    time.sleep(0.1)
    print(temp)