# Imperial College EEE - ELEC60013 Embedded Systems
## Aquapolis

We often focus on the scarcity of water, yet the quality of it is as problematic: unsafe
water is in the top 15 causes of death worldwide, counting more than 1.2 million
victims only in 2017, as a study by the OurWorldInData highlights. This does not
affect only rural areas but also urban ones, as in the recent case of the Flint Water
Crisis.

In addition to health implications, this represents an environmental and econom-
ical problem as well: as reported from the CDP Global Water Report 2020, water
security is a necessary issue to solve in order to achieve our Net Zero Goal and the
multiple studies indicates how the financial impact of water risks is more than 5
times greater than the cost of addressing them.

The first step to solve this problem is to have a closer insight into the quality of the
water globally, integrating the data sets already present with new data collected by
individuals and institutions on a local scale. We believe that only through collective
intelligence we can assure our model and predictions are up to date and can meet
the highest quality standards.

From this vision was born AquaPolis, a network of IoT water sensors that can pro-
vide an accessible solution both in the immediate and long-term future. Each de-
vice can collect measurements of the water’s quality at any time, generating predic-
tions on its potability based on a Machine Learning Model trained on big, verified
data sets. In addition, the new data, uploaded on a map, helps the model make bet-
ter predictions in the future, keeping track of the values locally and creating a more
accurate view of the water situation globally.


## Requirements

- [Raspberry Pi Zero W](https://www.raspberrypi.com/products/raspberry-pi-zero-w/)
- [CQRobot Ocean - TDS Sensor](https://www.amazon.co.uk/CQRobot-Ocean-Compatible-Scientific-Laboratory/dp/B08KXRHK7H/ref=asc_df_B08KXRHK7H/?tag=googshopuk-21&linkCode=df0&hvadid=463156464627&hvpos=&hvnetw=g&hvrand=10496818325336570027&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1006886&hvtargid=pla-1105654156265&psc=1)
- [Gravity - Analog Turbidity Sensor](https://thepihut.com/products/gravity-analog-turbidity-sensor-for-arduino)
- [RGB LED - Common Anode](https://www.switchelectronics.co.uk/rgb-5mm-led-common-anode?gclid=CjwKCAiAyPyQBhB6EiwAFUuaknjoZDOvCiegB7PQRNGGT4M-8GdJmlnJEkNEyYxgr4OTNf9sPEa3QhoCVQYQAvD_BwE)
- Button
- Python Modules
  - [Threading](https://docs.python.org/3.9/library/threading.html)
  - [Time](https://docs.python.org/3.9/library/time.html)
  - [smbus2](https://pypi.org/project/smbus2/)
  - [paho-mqtt](https://pypi.org/project/paho-mqtt/)
  - [datatime](https://docs.python.org/3.9/library/datetime.html)
  - [json](https://docs.python.org/3.9/library/json.html)
  - [dateutil](https://dateutil.readthedocs.io/en/stable/)
  - [requests](https://pypi.org/project/requests/)
  - local - [TDS](https://github.com/mp619/Aqua-Polis/blob/master/Main/TDS.py)
  - local - [Turbidity](https://github.com/mp619/Aqua-Polis/blob/master/Main/Turbidity.py)
  - local - [RGB](https://github.com/mp619/Aqua-Polis/blob/master/Main/RGB.py)

## Setup
- Connect components to approtiate pins on to the Raspberry Pi
- [Download](https://www.python.org/downloads/) and install Python 3.9
- Install relevent external modules
- Transfer \Main to Raspberry Pi
- Run main2.py containing full program

## Additonal Reference
- Please see [ADS1115](https://www.ti.com/lit/ds/symlink/ads1114.pdf?ts=1646227673693&ref_url=https%253A%252F%252Fwww.google.co.za%252F) datasheet for further reading into sensor register intialization via I2C

## Links
