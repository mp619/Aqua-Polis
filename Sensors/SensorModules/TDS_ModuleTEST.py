import time
import TDS

#State address of ADC
ADC_adr = 0x48

TDS.init()
TDS.config()

while True:
    total = 0
    for i in range(0,100):
        t1 = TDS.read(ADC_adr)
        time.sleep(0.01)
        total = total + t1
    avg = total/100
    tds = TDS.convert(avg)
    print(tds, 'ppm') 