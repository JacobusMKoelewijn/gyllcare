from gyllcare.config import IN_PRODUCTION
from gyllcare.config import ROOT_DIR
from gyllcare import create_logger
from picamera import PiCamera
from time import sleep

# The camera module contains a time out error which is difficult to resolve.
# A work around is to make use of aa try/except block.

log = create_logger(__name__)

if IN_PRODUCTION:
    def get_picture():
        sleep(5)

        camera = PiCamera()
        camera.rotation = 180
        camera.resolution = (2592, 1944)
        try:
            camera.start_preview()
            sleep(5)
            camera.capture(ROOT_DIR + '/app/static/Resources/img/fishlens.jpg')
            log.info("An Image has been captured.")
            camera.stop_preview()
        except Exception as e:
            log.error(e)
        finally:
            camera.close()
else:
    def get_picture():
        print("Development mode: Image has been captured.")