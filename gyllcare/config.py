import os
from key import keys

IN_PRODUCTION = False
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = False
SECRET_KEY = keys.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = keys.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False
TEMPLATES_AUTO_RELOAD = True
MAIL_SERVER = keys.get('MAIL_SERVER')
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = keys.get('MAIL_USERNAME')
MAIL_PASSWORD = keys.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = keys.get('MAIL_DEFAULT_SENDER')
MAIL_ASCII_ATTACHMENTS = False