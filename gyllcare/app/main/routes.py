from . import main
from gyllcare.config import IN_PRODUCTION
from gyllcare.config import ROOT_DIR
from .models import User, Events, Schedule
from .forms import LoginForm, ScheduleForm
from .base import CO2_scheduler, O2_scheduler, Light_scheduler, Therm_scheduler, schedule, CO2, O2, Therm, Light, alarm
from .extensions import db, mail, socketio
from .gpio import return_status
from .camera import get_picture
from flask_socketio import send
from datetime import datetime
from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user
import time
from flask_mail import Message
import subprocess
from key import keys

from gyllcare import create_logger

log = create_logger(__name__)

if IN_PRODUCTION:
    from .temp import read_temp
    from .pH import read_pH
else:
    def read_temp():
        return(40)

    def read_pH(cmd):
        return(6.000)


@main.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    user = User.query.filter_by(username="JMKoelewijn").first() 
    if request.method == "POST":
        if form.validate_on_submit():
            if User.query.first().username == form.name.data and User.query.first().password == form.password.data:
                login_user(user)
                log.info(f'{form.name.data} has logged in Gyllcare.')
                return redirect(url_for("main.gyllcare"))

    return render_template("login.html", form=form)

@main.route("/gyllcare", methods=["GET", "POST"])
@login_required
def gyllcare():

    schedule_form = ScheduleForm()
    event_start = Events.query.filter_by(id=1).first()
    event_clean = Events.query.filter_by(id=2).first()

    change_event_start_to_datetime = datetime.strptime(event_start.time, '%d-%m-%Y %H:%M')
    change_event_clean_to_datetime = datetime.strptime(event_clean.time, '%d-%m-%Y %H:%M')

    time_since_start = datetime.now().replace(microsecond=0) - change_event_start_to_datetime.replace(microsecond=0)
    time_since_clean = datetime.now().replace(microsecond=0) - change_event_clean_to_datetime.replace(microsecond=0)
    
    print(type(time_since_start))
    temperature = read_temp()
    pH = read_pH("R")

    if request.method == "POST":

        if CO2_scheduler.return_status():
            Schedule.query.filter_by(id=1).first().time_on = schedule_form.unit_co2_on.data
            Schedule.query.filter_by(id=1).first().time_off = schedule_form.unit_co2_off.data
            schedule.reschedule_job("toggle_CO2_on", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_co2_on.data +':00')
            schedule.reschedule_job("toggle_CO2_off", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_co2_off.data +':00')
        
        if O2_scheduler.return_status():
            Schedule.query.filter_by(id=2).first().time_on = schedule_form.unit_o2_on.data
            Schedule.query.filter_by(id=2).first().time_off = schedule_form.unit_o2_off.data
            schedule.reschedule_job("toggle_O2_on", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_o2_on.data +':00')
            schedule.reschedule_job("toggle_O2_off", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_o2_off.data +':00')
        
        if Light_scheduler.return_status():
           Schedule.query.filter_by(id=3).first().time_on = schedule_form.unit_light_on.data
           Schedule.query.filter_by(id=3).first().time_off = schedule_form.unit_light_off.data
           schedule.reschedule_job("toggle_light_on", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_light_on.data +':00')
           schedule.reschedule_job("toggle_light_off", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_light_off.data +':00')

        if Therm_scheduler.return_status():
             Schedule.query.filter_by(id=4).first().time_on = schedule_form.unit_temp_on.data
             Schedule.query.filter_by(id=4).first().time_off = schedule_form.unit_temp_off.data
             schedule.reschedule_job("toggle_temp_on", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_temp_on.data +':00')
             schedule.reschedule_job("toggle_temp_off", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_temp_off.data +':00')
        
        db.session.commit()

    schedule_form.unit_co2_on.default = Schedule.query.filter_by(id=1).first().time_on
    schedule_form.unit_co2_off.default = Schedule.query.filter_by(id=1).first().time_off
    schedule_form.unit_o2_on.default = Schedule.query.filter_by(id=2).first().time_on
    schedule_form.unit_o2_off.default = Schedule.query.filter_by(id=2).first().time_off
    schedule_form.unit_light_on.default = Schedule.query.filter_by(id=3).first().time_on
    schedule_form.unit_light_off.default = Schedule.query.filter_by(id=3).first().time_off
    schedule_form.unit_temp_on.default = Schedule.query.filter_by(id=4).first().time_on
    schedule_form.unit_temp_off.default = Schedule.query.filter_by(id=4).first().time_off
     
    schedule_form.process()

    return render_template("gyllcare.html",
                                          time_since_start=time_since_start,
                                          time_since_clean=time_since_clean,
                                          schedule_form=schedule_form,
                                          temperature=temperature,
                                          pH=pH,
                                          )

@main.route("/fishlens", methods=["GET", "POST"])
@login_required
def fishlens():
    get_picture()
    return ''



@main.route("/status", methods=["GET", "POST"])
@login_required
def status():

    CO2_schedule = Schedule.query.filter_by(id=1).first().active
    O2_schedule = Schedule.query.filter_by(id=2).first().active
    light_schedule = Schedule.query.filter_by(id=3).first().active
    temp_schedule = Schedule.query.filter_by(id=4).first().active

    gpio_14, gpio_15, gpio_18, gpio_23, gpio_16, gpio_20 = return_status()
    
    message = {
        'gpio_pin_14':gpio_14,
        'gpio_pin_15':gpio_15,
        'gpio_pin_18':gpio_18,
        'gpio_pin_23':gpio_23, 
        'gpio_pin_16':gpio_16, 
        'gpio_pin_20':gpio_20,
        'CO2_schedule':CO2_schedule,
        'O2_schedule':O2_schedule,
        'light_schedule':light_schedule,
        'temp_schedule':temp_schedule
               }

    switch_dictionary = {
        'CO2': CO2.toggle_state,
        'O2': O2.toggle_state,
        'Light': Light.toggle_state,
        'Therm': Therm.toggle_state,
        'CO2_schedule': CO2_scheduler.toggle_state,
        'O2_schedule': O2_scheduler.toggle_state,
        'light_schedule': Light_scheduler.toggle_state,
        'temp_schedule' : Therm_scheduler.toggle_state
        }

    if request.method == "POST":
        switch_name = request.get_json()["name"]
        switch_dictionary[str(switch_name)]()
        return ""
    
    schedule.print_jobs()

    return jsonify(message)

@main.route("/email", methods=["POST"])
@login_required
def email():
    if request.method == "POST":

        msg = Message("Gyllcare has send you a message", recipients=[keys.get('MAIL_RECIPIENT')])
        msg.body = "Attached you'll find the Gyllcare.log file."

        with main.open_resource(ROOT_DIR + "/data/gyllcare.log") as attach:
            msg.attach("gyllcare.log", "text/plain", attach.read())
        
        mail.send(msg)

        time.sleep(2)

        return ""

@main.route("/shutdown", methods=["POST"])
@login_required
def shutdown():
    if request.method == "POST":

        clean_aquarium = Events.query.filter_by(id=2).first()
        clean_aquarium.time = datetime.now().strftime("%d-%m-%Y %H:%M")
        db.session.commit()

        command_1 = "sudo pkill gunicorn"
        command_2 = "sudo service nginx stop"
        command_3 = "sudo shutdown -h now"
        
        subprocess.call(command_1.split())
        time.sleep(5)
        subprocess.call(command_2.split())
        time.sleep(5)
        subprocess.call(command_3.split())
        
        log.info("Shutting down Gyllcare for cleaning.")

        return ""

@main.route("/alarm_mode", methods=["POST"])
@login_required
def alarm_mode():
    if request.method == "POST":
  
        gpio_16 = return_status()[-2]

        if not gpio_16:
            alarm.start()
        else:
            alarm.stop()
        
        return jsonify(not gpio_16)

@socketio.on('message')
def receive_message(message):
    print(f'{message}')
    send('####### Greetings from Gyllcare...')


@main.route("/logout")
@login_required
def logout():
    logout_user()
    log.info("User has logged out")
    return redirect(url_for("main.index"))