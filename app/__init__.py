from flask import Flask

from .main.base import read_temp_plot_data, schedule, CO2, O2, Therm, Light
from .main.models import Events, Schedule
from .main.camera import get_picture

from datetime import datetime
# import eventlet

from .main import main as main_blueprint
from .main.extensions import db, socketio, mail, login_manager


def create_app(config_file='config.py'):

    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    
    # eventlet.monkey_patch()
    login_manager.login_view = "main.index"
    
    get_picture()
    
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    # socketio.init_app(app)

    with app.app_context():
        # print("initiating")
        
        app_start = Events.query.filter_by(id=1).first()
        app_start.time = datetime.now().strftime("%d-%m-%Y %H:%M")
        db.session.commit()

        unit_co2_time_on = Schedule.query.filter_by(id=1).first().time_on
        unit_co2_time_off = Schedule.query.filter_by(id=1).first().time_off
        unit_o2_time_on = Schedule.query.filter_by(id=2).first().time_on
        unit_o2_time_off = Schedule.query.filter_by(id=2).first().time_off
        unit_light_time_on = Schedule.query.filter_by(id=3).first().time_on
        unit_light_time_off = Schedule.query.filter_by(id=3).first().time_off
        unit_temp_time_on = Schedule.query.filter_by(id=4).first().time_on
        unit_temp_time_off = Schedule.query.filter_by(id=4).first().time_off

        schedule.add_job(CO2.switch_on,'interval', days=1, start_date='2021-05-01 ' + unit_co2_time_on +':00', id="toggle_CO2_on")
        schedule.add_job(CO2.switch_off,'interval', days=1, start_date='2021-05-01 ' + unit_co2_time_off +':00', id="toggle_CO2_off")
        schedule.add_job(O2.switch_on,'interval', days=1, start_date='2021-05-01 ' + unit_o2_time_on +':00', id="toggle_O2_on")
        schedule.add_job(O2.switch_off,'interval', days=1, start_date='2021-05-01 ' + unit_o2_time_off +':00', id="toggle_O2_off")
        schedule.add_job(Light.switch_on,'interval', days=1, start_date='2021-05-01 ' + unit_light_time_on +':00', id="toggle_light_on")
        schedule.add_job(Light.switch_off,'interval', days=1, start_date='2021-05-01 ' + unit_light_time_off +':00', id="toggle_light_off")
        schedule.add_job(Therm.switch_on,'interval', days=1, start_date='2021-05-01 ' + unit_temp_time_on +':00', id="toggle_temp_on")
        schedule.add_job(Therm.switch_off,'interval', days=1, start_date='2021-05-01 ' + unit_temp_time_off +':00', id="toggle_temp_off")
        schedule.add_job(read_temp_plot_data,'interval', minutes=60, start_date='2021-05-01 00:00:00', id="read_temp_plot_data")

        schedule.start()

        app.register_blueprint(main_blueprint)

        logfile = open("/home/pi/Desktop/logs/Gyllcare_log.txt", "a")
        logfile.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " ###### Gyllcare has been initiated. \n")
        logfile.close()

        return app