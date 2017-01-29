#       The wiki suggests the following sensor values:
#               Min  Typ  Max  Condition
#               0    0    0    sensor in open air
#               0    20   300  sensor in dry soil
#               300  580  700  sensor in humid soil
#               700  940  950  sensor in water
# grovepi.digitalWrite(relay_1,1) - One on, zero  off

import time
import grovepi
from grove_rgb_lcd import *

# Set pins for variouse connected grove devices. Disable moist sensors & relay according to how
# many of them you have configured
ultrasonic_ranger = 2
moist_sens_1 = 0
#moist_sens_2 = 0
dht_sensor_port = 8
dht_sensor_type = 0

time.sleep(1)

while True:
    try:
        print "Water Level:" + grovepi.ultrasonicRead(ultrasonic_ranger)
        print "Moisture Levels:" + grovepi.analogRead(moist_sens_1) + "/" + grovepi.analogRead(moist_sens_2)
        time.sleep(5)

    except KeyboardInterrupt:
        break
    except IOError:
        print ("Error")
