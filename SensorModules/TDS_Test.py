import time
import TDS
import Turbidity as Turb

#State address of ADC
ADC_adr = 0x48

bus = TDS.init()
TDS.config(bus, ADC_adr)
Turb.config(bus, ADC_adr)

while True:
    total_TDS = 0
    total_Turb = 0
    for i in range(0,100):
        TDS.config(bus, ADC_adr)
        t1 = TDS.read(bus, ADC_adr)
        print(t1)
        time.sleep(0.01)
        Turb.config(bus, ADC_adr)
        t2 = Turb.read(bus, ADC_adr)
        print(t2)
        time.sleep(0.01)
        total_TDS = total_TDS + t1
        total_Turb = total_Turb + t2
    avg_TDS = total_TDS/100
    avg_Turb = total_Turb/100
    tds = TDS.convert(avg_TDS)
    turb = Turb.convert(avg_Turb)
    print(tds, 'ppm', turb, 'NTU') 