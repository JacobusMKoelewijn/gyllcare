####################################
########## Gyllcare v 1.0  #########
########## J. M. Koelewijn #########
####################################

from app import create_app
from app.main.extensions import socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app)