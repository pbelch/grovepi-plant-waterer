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

ledbar = 7
ultrasonic_ranger = 2
moist_sens_1 = 0
#moist_sens_2 = 0
relay_1 = 3
relay_2 = 4
dht_sensor_port = 8
dht_sensor_type = 0

grovepi.pinMode(ledbar,"OUTPUT")
grovepi.pinMode(relay_1,"OUTPUT")
grovepi.pinMode(relay_2,"OUTPUT")
setRGB(0,255,0)
timeSinceWater = 0

# Set your trigger thresholds here. Will require some expermineting depending
# on the size and depth of your water resovior

##### turn values to int?

moistureLevelTrigger = 450 # Levelunderwhich water event will trigger
minWaterLevel = 15 # Minimum water remaining before water events stop
maxWaterLevel = 150
minWaterGap = 10 # Minimum interval in mins between triggering a watering cycle
waterPumpDuration = 2 # Seconds to run pump for

time.sleep(1)

### RUN AS A BACKGROUND SCRIPT
while True:
    try:
        ledLevel = grovepi.ledBar_getBits(ledbar)
        waterDistance = grovepi.ultrasonicRead(ultrasonic_ranger)
        moistureOne = grovepi.analogRead(moist_sens_1)
        moistureTwo = grovepi.analogRead(moist_sens_2)
        [ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)

        # TODO - Check if are outside the minWaterGap since last watered - timeSinceWater
        # Check water level
        if waterDistance > minWaterGap:
            # if it is, check if we need to pump and do it
            if moistureOne < moistureLevelTrigger and moist_sens_1:
                grovepi.digitalWrite(relay_1,1)
                time.sleep(waterPumpDuration)
                grovepi.digitalWrite(relay_1,0)
            if moistureTwo < moistureLevelTrigger and moist_sens_2:
                grovepi.digitalWrite(relay_2,1)
                time.sleep(waterPumpDuration)
                grovepi.digitalWrite(relay_2,0)

            #disply time, temp and water level. Update LED bar
            setText("Temp":  + str(temp) + " Hum: " + str(hum))

        else:
            print "Water level too low to do anything. Log to text file"
            setText("Temp":  + str(temp) + " Hum: " + str(hum) + "WATER TOO LOW!!")

        #Write ledbar level nased on a case statement
        segment = int(round((maxWaterLevel - minWaterLevel) / 10))
        barlevel =  int(round((waterDistance  - minWaterLevel)  / segment))
        grovepi.ledBar_setLevel(ledbar, barlevel)

        # Add a logging if. If enabled, write log with run determination

        #TODO- Set to 15 mins after testing
        time.sleep(5)

    except KeyboardInterrupt:
        grovepi.ledBar_setBits(ledbar, 0)
        grovepi.digitalWrite(relay_1,0)
        grovepi.digitalWrite(relay_2,0)
        break
    except IOError:
        print ("Error")
