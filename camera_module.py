from picamera import PiCamera
from time import sleep

def get_picture():
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (2592, 1944)
    camera.start_preview()
    sleep(5)
    camera.capture('/var/www/html/gyllcare/static/Resources/img/fishlens.jpg')
    # camera.capture('/home/pi/Viinum/gyllcare/static/Resources/img/fishlens.jpg')
    camera.stop_preview()
    # print("picture taken")