from app.config import IN_DEVELOPMENT_MODE

from picamera import PiCamera
from time import sleep

if not IN_DEVELOPMENT_MODE:

    # The camera module contains a time out error which has to be resolved!
    # For now the solution is to put it in a try/error block (as is proper python code)

    def get_picture():
        sleep(5)
        print("picture is taken")

        camera = PiCamera()
        camera.rotation = 180
        camera.resolution = (2592, 1944)
        try:
            camera.start_preview()
            sleep(5)
            print("Camera will now capture")
            camera.capture('/var/www/html/gyllcare/app/static/Resources/img/fishlens.jpg')
            # camera.capture('/home/pi/Viinum/gyllcare/app/static/Resources/img/fishlens.jpg')
            camera.stop_preview()
        finally:
            camera.close()
        # print("Camera closed confirmed")

if IN_DEVELOPMENT_MODE:
    def get_picture():
        print("Development mode: Image has been captured.")
        