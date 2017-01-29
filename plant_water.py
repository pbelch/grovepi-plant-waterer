import time
import grovepi
from grove_rgb_lcd import *
import datetime
import file
# Configuration required if using API post.
try:
    from urllib.parse import urlparse, urlencode
except ImportError:
     from urlparse import urlparse
     from urllib import urlencode
try:
    from urllib.request import Request, urlopen
except ImportError:
     import urllib2
     from urllib2 import Request
     from urllib2 import urlopen

# Set pins for variouse connected grove devices. Disable moist sensors & relay according to how
# many of them you have configured
ledbar = 7
ultrasonic_ranger = 2
moist_sens_1 = 0
#moist_sens_2 = 0
relay_1 = 3
#relay_2 = 4
dht_sensor_port = 8
dht_sensor_type = 0


# Set your trigger thresholds here. Will require some expermineting depending
# on the size and depth of your water resovior. Run calbiraton script to help you out
moistureLevelTrigger = 450 # Levelunderwhich water event will trigger
minWaterLevel = 15 # Minimum water remaining before water events stop
maxWaterLevel = 150
minWaterGap = 10 # Minimum interval in mins between triggering a watering cycle
waterPumpDuration = 2 # Seconds to run pump for
logging = 1 # Set 1 for enabled, 0 for disabled

# Configuration required if you want to log results to an api
sendtoApi = 1 # Set 1 for enabled, 0 for disabled
postUrl = "https://my.api.url.com"

#Set GPIO communicaion type on app startup
grovepi.pinMode(ledbar,"OUTPUT")
grovepi.pinMode(relay_1,"OUTPUT")
grovepi.pinMode(relay_2,"OUTPUT")
lastWateredOne = 0;
lastWateredTwo = 0;
time.sleep(1)

while True:
    try:
        ledLevel = grovepi.ledBar_getBits(ledbar)
        waterDistance = grovepi.ultrasonicRead(ultrasonic_ranger)
        moistureOne = grovepi.analogRead(moist_sens_1)
        moistureTwo = grovepi.analogRead(moist_sens_2)
        [ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)
        current_time = datetime.datetime.now(datetime.timezone.utc)
        unix_timestamp = current_time.timestamp()

        # Check water level. if it is ok, check if we need to pump and do it
        if waterDistance > minWaterGap:
            setRGB(0,255,0)
            if lastWateredOne > (unix_timestamp - 900):
                if moistureOne < moistureLevelTrigger and moist_sens_1:
                    grovepi.digitalWrite(relay_1,1)
                    time.sleep(waterPumpDuration)
                    grovepi.digitalWrite(relay_1,0)
                    lastWateredOne = current_time.timestamp()
                # TODO - Check if are outside the minWaterGap since last watered - lastWatered
            if lastWateredTwo > (unix_timestamp - 900):
                if moistureTwo < moistureLevelTrigger and moist_sens_2:
                    grovepi.digitalWrite(relay_2,1)
                    time.sleep(waterPumpDuration)
                    grovepi.digitalWrite(relay_2,0)
                    lastWateredTwo = current_time.timestamp()
            #disply time, temp and water level. Update LED bar
            setText("Temp":  + str(temp) + " Hum: " + str(hum))
        else:
            setRGB(255,0,0)
            print "Water level too low to do anything. Log to text file"
            setText("Temp":  + str(temp) + " Hum: " + str(hum) + "WATER TOO LOW!!")

        #Write ledbar level nased on a case statement
        segment = int(round((maxWaterLevel - minWaterLevel) / 10))
        barlevel =  int(round((waterDistance  - minWaterLevel)  / segment))
        grovepi.ledBar_setLevel(ledbar, barlevel)

        # Add a logging if. If enabled, write log with run determination
        if logging > 0 :
            timestr = time.strftime("%Y%m%d")
            outputfile = "./logs/" + timestr + ".txt"
            with open(outputfile, "w") as text_file:
                print(unix_timestamp + ":" + " Water Level:" + waterDistance + " Moisture Levels:" +
                    moistureOne + "/" + moistureTwo + " Last Watered:" + lastWateredOne + "/" + lastWateredTwo + "\n")
        if sendtoApi > 0 :
            url = (postUrl)
            post_fields = {
                'temp': XXX,
                'hum': XXX,
                'moistOne': XXX,
                'moistTwo': XXX,
                'waterLevel': XXX
            }     # Set POST fields here
            request = Request(url, urlencode(post_fields).encode())
            urlopen(request)

        #TODO- Set to 15 mins after testing (900)
        time.sleep(5)

    except KeyboardInterrupt:
        grovepi.ledBar_setBits(ledbar, 0)
        grovepi.digitalWrite(relay_1,0)
        grovepi.digitalWrite(relay_2,0)
        break
    except IOError:
        print ("Error")
