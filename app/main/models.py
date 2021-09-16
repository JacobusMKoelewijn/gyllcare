from .extensions import db, login_manager
from flask_login import UserMixin

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(30), unique=True)
    time = db.Column(db.String(30), unique=True)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(30), unique=True)
    active = db.Column(db.Boolean)
    time_on = db.Column(db.String(30), unique=False)
    time_off = db.Column(db.String(30), unique=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))