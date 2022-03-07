from flask import Blueprint

main = Blueprint('main', __name__)

from . import base, routes, extensions, forms, gpio, camera, temp, models
