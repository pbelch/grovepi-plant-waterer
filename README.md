STILL WORK IN PROGRESS. PLS CHECK BACK SOON

#grovepi-plant-waterer

#TODO
- Check where grovePI can be installed vs plant water script
- Test calibration script
- Add option to log metrics to an api (and make api!)

# Installing grovePI & waterer script
###grovepi

### Calibration
The 'calibrate.py' script will log out the current water and moisture level every 5 seconds. Configure pin values to the
same as in the main 'plant_waterer.py', and fill water to just above the pump to determine low level limit, and to a safe
lax level that doesn't cause splash onto the sensor to determine top level <br/><br/>
For moisture sensors, water you plant to the optimum level, and record that value as the moisture level

###Additional Features
******* comment in for second waterer, waterer and logging *****

### Running the script in the background
Make the script executable:
```python
chmod +x plant_waterer.py
```
Create a cron job to run the script each time the pi starts:
```python
sudo crontab -e
@reboot python /home/pi/plant_waterer.py &
```
You can then view the process ID should you need to force quit using:
```python
ps ax | grep plant_waterer.py
```
