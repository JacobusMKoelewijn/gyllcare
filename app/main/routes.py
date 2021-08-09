from . import main

from .models import User, Events, Schedule
from .forms import LoginForm, ScheduleForm
from .base import schedule, CO2, O2, Therm, Light, alarm
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



@main.route("/", methods=["GET", "POST"])
def index():
    time = datetime.now().strftime(("%d/%m/%Y"))
    form = LoginForm()
    user = User.query.filter_by(username="JMKoelewijn").first() 
    if request.method == "POST":
        if form.validate_on_submit():
            if User.query.first().username == form.name.data and User.query.first().password == form.password.data:
                login_user(user)
                return redirect(url_for("main.gyllcare"))

    return render_template("login.html", form=form, time=time)

@main.route("/gyllcare", methods=["GET", "POST"])
@login_required
def gyllcare():

    schedule_form = ScheduleForm()
    results = Events.query.filter_by(id=1).first()
    change_to_datetime = datetime.strptime(results.time, '%d-%m-%Y %H:%M')
    time_active = str(datetime.now().replace(microsecond=0) - change_to_datetime.replace(microsecond=0))[:-3] 
    # temperature = read_temp()
    # time_span = x_data[-1]

    if request.method == "POST":
        Schedule.query.filter_by(id=1).first().time_on = schedule_form.unit_co2_on.data
        Schedule.query.filter_by(id=1).first().time_off = schedule_form.unit_co2_off.data
        Schedule.query.filter_by(id=2).first().time_on = schedule_form.unit_o2_on.data
        Schedule.query.filter_by(id=2).first().time_off = schedule_form.unit_o2_off.data
        Schedule.query.filter_by(id=3).first().time_on = schedule_form.unit_light_on.data
        Schedule.query.filter_by(id=3).first().time_off = schedule_form.unit_light_off.data
        Schedule.query.filter_by(id=4).first().time_on = schedule_form.unit_temp_on.data
        Schedule.query.filter_by(id=4).first().time_off = schedule_form.unit_temp_off.data
        
        db.session.commit()

        schedule.reschedule_job("CO2.switch_on", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_co2_on.data +':00')
        schedule.reschedule_job("CO2.switch_off", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_co2_off.data +':00')
        schedule.reschedule_job("O2.switch_on", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_o2_on.data +':00')
        schedule.reschedule_job("O2.switch_off", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_o2_off.data +':00')
        schedule.reschedule_job("Light.switch_on", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_light_on.data +':00')
        schedule.reschedule_job("Light.switch_off", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_light_off.data +':00')
        schedule.reschedule_job("Therm.switch_on", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_temp_on.data +':00')
        schedule.reschedule_job("Therm.switch_off", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_temp_off.data +':00')

    
    schedule_form.unit_co2_on.default = Schedule.query.filter_by(id=1).first().time_on
    schedule_form.unit_co2_off.default = Schedule.query.filter_by(id=1).first().time_off
    schedule_form.unit_o2_on.default = Schedule.query.filter_by(id=2).first().time_on
    schedule_form.unit_o2_off.default = Schedule.query.filter_by(id=2).first().time_off
    schedule_form.unit_light_on.default = Schedule.query.filter_by(id=3).first().time_on
    schedule_form.unit_light_off.default = Schedule.query.filter_by(id=3).first().time_off
    schedule_form.unit_temp_on.default = Schedule.query.filter_by(id=4).first().time_on
    schedule_form.unit_temp_off.default = Schedule.query.filter_by(id=4).first().time_off
    
    schedule_form.process()

    return render_template("gyllcare.html", #Is this still required after vanilla js update?
                                          time_active=time_active,
                                          schedule_form=schedule_form,
                                        #   temperature=temperature,
                                          )

@main.route("/fishlens", methods=["GET", "POST"])
@login_required
def fishlens():
    get_picture()
    return ''


@main.route("/status", methods=["GET", "POST"])
@login_required
def status():

    gpio_14, gpio_15, gpio_18, gpio_23, gpio_16 = return_status()
    message = {'gpio_pin_14':gpio_14,'gpio_pin_15':gpio_15,'gpio_pin_18':gpio_18,'gpio_pin_23':gpio_23, 'gpio_pin_16':gpio_16}
    switch_dictionary = {'CO2': CO2.toggle_state, 'O2': O2.toggle_state, 'Light': Light.toggle_state, 'Therm': Therm.toggle_state}

    if request.method == "POST":
        switch_name = request.get_json()["name"]
        switch_dictionary[str(switch_name)]()
        return ""
    
    return jsonify(message)

@main.route("/email", methods=["POST"])
@login_required
def email():
    if request.method == "POST":

        schedulefile = open("/home/pi/Desktop/logs/Schedule_log.txt", "w")

        for i in schedule.get_jobs():
            schedulefile.write(str(i) + "\n")
        schedulefile.close()
 
        msg = Message("Gyllcare has send you a message", recipients=["mklwn@hotmail.com"])
        msg.body = "Attached you'll find the Gyllcare log files"

        with main.open_resource("/home/pi/Desktop/logs/Gyllcare_log.txt") as attach:
            msg.attach("Gyllcare_log.txt", "text/plain", attach.read())
        with main.open_resource("/home/pi/Desktop/logs/Schedule_log.txt") as attach_2:
            msg.attach("Schedule_log.txt", "text/plain", attach_2.read())
        
        
        mail.send(msg)

        time.sleep(2)
        print("succes")
        
        return ""

@main.route("/shutdown", methods=["POST"])
@login_required
def shutdown():
    if request.method == "POST":
        command_1 = "sudo service apache2 stop"
        command_2 = "sudo shutdown -h now"
        command_dev = "echo works"
        # subprocess.call(command_1.split())
        # subprocess.call(command_2.split())
        subprocess.call(command_dev.split())
        print("shutting down")
        return "OK"

@main.route("/alarm_mode", methods=["POST"])
@login_required
def alarm_mode():
    if request.method == "POST":

        # socketio.emit('alarm', 'the alarm has been triggered')
   
        gpio_16 = return_status()[-1]


        if not gpio_16:
            alarm.start()
        else:
            alarm.stop()
        
        return jsonify(not gpio_16)

# @socketio.on('message')
# def receive_message(message):
#     print(f'####### {message}')
#     send('This is a message from the server side!')


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))