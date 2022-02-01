####################################
########## Gyllcare v 1.0  #########
########## J. M. Koelewijn #########
####################################

from app import create_app
from app.main.extensions import socketio
from app.config import IN_DEVELOPMENT_MODE


# Initiate finalizatin of project.

# When using Apache2
app = create_app()

if IN_DEVELOPMENT_MODE and __name__ == '__main__':
    socketio.run(app)
    print("Starting up in development mode.")

print("####### Gyllcare seems to work.. awaiting response from the browser")

# switched to eventlet 0.30.2
# switched to gevent
# gunicorn --worker-class eventlet -b 192.168.178.57:9000 -t 120 'gyllcare:create_app()'