import RPi.GPIO as GPIO
import time
from datetime import datetime
from .extensions import socketio

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)  # Relay switches
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(20, GPIO.OUT, initial=GPIO.LOW)  # blue LED
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)  # red LED
GPIO.setup(21, GPIO.IN)                     # PIR Sensor

class ToggleSwitch:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.state = GPIO.input(self.id)

    def toggle_state(self):
        if self.state == 0:
            GPIO.output(self.id, GPIO.HIGH)
            self.state = GPIO.input(self.id)
            self.log("manually")

        elif self.state == 1:
            GPIO.output(self.id, GPIO.LOW)
            self.state = GPIO.input(self.id)
            self.log("manually")

    def switch_on(self):
        GPIO.output(self.id, GPIO.HIGH)
        self.log("as scheduled")

    def switch_off(self):
        GPIO.output(self.id, GPIO.LOW)
        self.log("as scheduled")

    def log(self, operation):
        logfile = open("/home/pi/Desktop/logs/Gyllcare_log.txt", "a")
        logfile.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " ### The " + self.name + " unit has been turned " + ("on " if self.state == 1 else "off ") + operation + ". \n")
        logfile.close()


def return_status(): # return current status of GPIO pins.
    gpio_status = [True if item == 1 else False for item in [GPIO.input(14), GPIO.input(15), GPIO.input(18), GPIO.input(23), GPIO.input(16)]]
    return gpio_status    

def alarm_on(stop):
    logfile = open("/home/pi/Desktop/logs/Gyllcare_log.txt", "a")
    logfile.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " ### Motion detector has been switched on. \n")
    logfile.close()
    GPIO.output(16, GPIO.HIGH)
    while True:
        if GPIO.input(21):

            socketio.emit('alarm', 'the alarm has been triggered') 
            # -- FIX THIS AFTER HOLIDAY WITH NGYNX/GUNICORN OR A DIFFERENT APPROACH

            GPIO.output(20, GPIO.HIGH)
            logfile = open("/home/pi/Desktop/logs/Gyllcare_log.txt", "a")
            logfile.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " ### Some motion was detected! \n")
            logfile.close()
            time.sleep(5)
            GPIO.output(20, GPIO.LOW)
        time.sleep(1)
        if(stop()):
            GPIO.output(16, GPIO.LOW)
            break