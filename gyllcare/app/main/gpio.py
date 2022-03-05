import RPi.GPIO as GPIO
import time
from datetime import datetime
from .extensions import socketio
from gyllcare import create_logger

log = create_logger(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Relay switches

GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)  # CO2 
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)   # O2
GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)   # Main Light
GPIO.setup(1, GPIO.OUT, initial=GPIO.LOW)   # Temperature
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
        log.info(f"{self.name} unit has been turned {'on' if self.state == 1 else 'off'} {operation}.")


def return_status():
    """Return current status of GPIO pins."""
    gpio_status = [True if item == 1 else False for item in [GPIO.input(25), GPIO.input(8), GPIO.input(7), GPIO.input(1), GPIO.input(16), GPIO.input(20)]]
    return gpio_status    

def alarm_on(stop):
    """Activates the PIR Sensor"""
    log.info("Motion detector has been switched on.")
    GPIO.output(16, GPIO.HIGH)
    while True:
        if GPIO.input(21):
            GPIO.output(20, GPIO.HIGH)
            socketio.emit('alarm')
            log.info("Motion was detected!")
            time.sleep(5)
        time.sleep(1)

        if(stop()):
            GPIO.output(16, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            break