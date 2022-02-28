####################################
########## Gyllcare v 1.0  #########
########## J. M. Koelewijn #########
####################################

import os
from gyllcare.app import create_app
from gyllcare.app.main.extensions import socketio
from gyllcare.app.config import IN_PRODUCTION
from gyllcare.app.config import ROOT_DIR

# import gunicorn
# gunicorn.app
# Add infor regarding gunicorn and apache etc.
# Initiate finalizatin of project.
# print(IN_DEVELOPMENT_MODE)

# print(ROOT_DIR)


if not IN_PRODUCTION:
    if __name__ == '__main__':
        app = create_app()
        socketio.run(app)
        print("Starting in development mode.")

print("####### Gyllcare seems to work.. awaiting response from the browser")

# switched to eventlet 0.30.2
# switched to gevent
# gunicorn --worker-class eventlet -b 192.168.178.57:9000 -t 120 'gyllcare:create_app()'