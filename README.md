STILL WORK IN PROGRESS. PLS CHECK BACK SOON

#grovepi-plant-waterer

#TODO
- Check where grovePI can be installed vs plant water script
- calibration script
- add option to log metrics to an api

# Installing grovePI & waterer script

# Calibrating the waterer

# Running the script in the background
Make the script executable:
'''python
chmod +x plant_waterer.py
'''
Create a cron job to run the script each time the pi starts:
'''python
sudo crontab -e
'''
'''python
@reboot python /home/pi/plant_waterer.py &
'''
You can then view the process ID should you need to force quit using:
'''python
ps ax | grep test.py
'''
