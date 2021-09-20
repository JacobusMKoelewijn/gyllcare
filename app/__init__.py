from flask import Flask

from .main.base import read_temp_plot_data, schedule, CO2, O2, Therm, Light, CO2_scheduler, O2_scheduler, Therm_scheduler, Light_scheduler
from .main.models import Events, Schedule
# from .main.camera import get_picture

from datetime import datetime
import eventlet

from .main import main as main_blueprint
from .main.extensions import db, socketio, mail, login_manager



def create_app(config_file='config.py'):

    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    
    eventlet.monkey_patch()
    login_manager.login_view = "main.index"
       
    
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    with app.app_context():

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

        schedule.add_job(CO2.switch_on,'interval', days=1, start_date='2021-05-01 ' + unit_co2_time_on +':00', id="toggle_CO2_on", misfire_grace_time=120)
        schedule.add_job(CO2.switch_off,'interval', days=1, start_date='2021-05-01 ' + unit_co2_time_off +':00', id="toggle_CO2_off", misfire_grace_time=120)
        schedule.add_job(O2.switch_on,'interval', days=1, start_date='2021-05-01 ' + unit_o2_time_on +':00', id="toggle_O2_on", misfire_grace_time=120)
        schedule.add_job(O2.switch_off,'interval', days=1, start_date='2021-05-01 ' + unit_o2_time_off +':00', id="toggle_O2_off", misfire_grace_time=120)
        schedule.add_job(Light.switch_on,'interval', days=1, start_date='2021-05-01 ' + unit_light_time_on +':00', id="toggle_light_on", misfire_grace_time=120)
        schedule.add_job(Light.switch_off,'interval', days=1, start_date='2021-05-01 ' + unit_light_time_off +':00', id="toggle_light_off", misfire_grace_time=120)
        schedule.add_job(Therm.switch_on,'interval', days=1, start_date='2021-05-01 ' + unit_temp_time_on +':00', id="toggle_temp_on", misfire_grace_time=120)
        schedule.add_job(Therm.switch_off,'interval', days=1, start_date='2021-05-01 ' + unit_temp_time_off +':00', id="toggle_temp_off", misfire_grace_time=120)
        schedule.add_job(read_temp_plot_data,'interval', minutes=60, start_date='2021-05-01 00:00:00', id="read_temp_plot_data", misfire_grace_time=120)

        schedule.start()

        if not CO2_scheduler.return_status():
            CO2_scheduler.pause_schedule()
        
        if not O2_scheduler.return_status():
            O2_scheduler.pause_schedule()
        
        if not Light_scheduler.return_status():
            Light_scheduler.pause_schedule()

        if not Therm_scheduler.return_status():
            Therm_scheduler.pause_schedule()

        app.register_blueprint(main_blueprint)

        logfile = open("/home/pi/Desktop/logs/Gyllcare_log.txt", "a")
        logfile.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " ###### Gyllcare has been initiated. \n")
        logfile.close()

        return app