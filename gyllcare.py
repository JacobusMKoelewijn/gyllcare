####################################
########## Gyllcare v 1.0  #########
########## J. M. Koelewijn #########
####################################

from app import create_app
from app.main.extensions import socketio

print("####### Gyllcare seems to work.. awaiting response from the browser")

# app = create_app()

# if __name__ == '__main__':
    # app.run()
    # socketio.run(app)

# switched to eventlet 0.30.2
# gunicorn --worker-class eventlet -b 192.168.178.57:9000 -t 120 'gyllcare:create_app()'
