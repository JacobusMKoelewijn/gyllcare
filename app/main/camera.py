from picamera import PiCamera
from time import sleep

def get_picture():
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (2592, 1944)
    try:
        camera.start_preview()
        sleep(5)
        print("Madness 1")
        camera.capture('/var/www/html/gyllcare/app/static/Resources/img/fishlens.jpg')
        # camera.capture('/home/pi/Viinum/gyllcare/app/static/Resources/img/fishlens.jpg')
        print("Madness 2")
        camera.stop_preview()
        print("maddnes 3")
    finally:
        camera.close()
        print("maddnes 4")