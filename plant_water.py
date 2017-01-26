#       The wiki suggests the following sensor values:
#               Min  Typ  Max  Condition
#               0    0    0    sensor in open air
#               0    20   300  sensor in dry soil
#               300  580  700  sensor in humid soil
#               700  940  950  sensor in water
# grovepi.digitalWrite(relay_1,1) - One on, two off

import time
import grovepi
from grove_rgb_lcd import *

ledbar = 7
ultrasonic_ranger = 2
moist_sens_1 = 0
#moist_sens_2 = 0
relay_1 = 3
relay_2 = 4

grovepi.pinMode(ledbar,"OUTPUT")
grovepi.pinMode(relay_1,"OUTPUT")
grovepi.pinMode(relay_2,"OUTPUT")

time.sleep(1)
i = 0
setRGB(0,255,0)
while True:
    try:
        ledLevel = grovepi.ledBar_getBits(ledbar)
        waterDistance = grovepi.ultrasonicRead(ultrasonic_ranger)
        moistureOne = grovepi.analogRead(moist_sens_1)
        ## Check water level
        ###If water level is ok, check mositure sensor connected
        #### if it is, check if we need to pump and do it

        ##disply time, temp and water level. Update LED bar
        for i in range(0,11):
            #Write ledbar level
            grovepi.ledBar_setLevel(ledbar, i)

            #Write screen text
            setText("Current Position: " + str(i))
        time.sleep(.3)

    except KeyboardInterrupt:
        grovepi.ledBar_setBits(ledbar, 0)
        break
    except IOError:
        print ("Error")
