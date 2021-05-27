import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)

def return_status():
    gpio_status = ["on" if item == 1 else "off" for item in [GPIO.input(14), GPIO.input(15), GPIO.input(18), GPIO.input(23)]]
    return gpio_status
    # The current status of every GPIO pin is requested and returned.
    # Using a list comprehension every value of 1 is changed to "on" and 0 is changed to "off".

def toggle(state, gpio, name):
    if state == "true":
        GPIO.output(int(gpio[-2:]), GPIO.HIGH) 
        log(name, "on manually")
    elif state == "false":
        GPIO.output(int(gpio[-2:]), GPIO.LOW)
        log(name, "off manually")

def log(unit, state):
    logfile = open("/home/pi/Desktop/logs/Gyllcare_log.txt", "a")
    logfile.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " ### " + unit + " has been turned " + state + ". \n")
    logfile.close()

def toggle_CO2_on():
    GPIO.output(14, GPIO.HIGH)
    log("CO2 unit", "on as scheduled")

def toggle_CO2_off():
    GPIO.output(14, GPIO.LOW)
    log("CO2 unit", "off as scheduled")

def toggle_O2_on():
    GPIO.output(15, GPIO.HIGH)
    log("O2 unit", "on as scheduled")

def toggle_O2_off():
    GPIO.output(15, GPIO.LOW)
    log("O2 unit", "off as scheduled")

def toggle_light_on():
    GPIO.output(18, GPIO.HIGH)
    log("Main light unit", "on as scheduled")

def toggle_light_off():
    GPIO.output(18, GPIO.LOW)
    log("Main light unit", "off as scheduled")

def toggle_temp_on():
    GPIO.output(23, GPIO.HIGH)
    log("Temperature unit", "on as scheduled")

def toggle_temp_off():
    GPIO.output(23, GPIO.LOW)
    log("Temperature unit", "off as scheduled")