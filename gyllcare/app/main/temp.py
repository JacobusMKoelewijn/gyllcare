from gyllcare.app.config import IN_PRODUCTION

import os
import glob
import time

# To use DS18B20 temperature probe enable for 1-Wire interface.
# dtoverlay=w1-gpio
# Default GPIO4.
# circuitbasics.com/raspberry-pi-ds18B20-temperature-sensor-tutorial

if IN_PRODUCTION:
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    def read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
    
    def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return round(temp_c, 1)

if not IN_PRODUCTION:
    def read_temp():
        return 40.0

