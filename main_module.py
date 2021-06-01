#####################################
##########  Gyllcare v 1.0 ##########
########## J. M. Koelewijn ##########
#####################################

from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from gpio_module import toggle, return_status, toggle_CO2_on, toggle_CO2_off, toggle_O2_on, toggle_O2_off, toggle_light_on, toggle_light_off, toggle_temp_on, toggle_temp_off
from temp_module import read_temp
from datetime import datetime, timedelta
import subprocess

# Idea! create shutdown button that gives unix commands!!

# Libraries required to plot the temperature graph.
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
matplotlib.use('Agg')

from random import seed, random # For development
seed(1) # For development

# What does this do exactly? Needed after "RuntimeError: main thread is not in main loop. Related to Tkinter?"
# Had to install sudo apt install libatlas-base-dev to surpress a warning

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

app.config["SECRET_KEY"] = "WWOeeyV?cAnh"
# A conflict in session initiation was found when os.urandom(24) was used to generate a secret key. Problem disappears when a static secret key is used instead.

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://viinumco_JMKoelewijn:WWOeeyV?cAnh@viinum.com/viinumco_aquapi"
# An additional driver 'pymysql' has to be installed for the database connection to work.gyllcarel security. If not specified the browser might give a warning.
# No configuration for the CSRF token is being used. Not sure if this is necessary.

app.config["TEMPLATES_AUTO_RELOAD"] = True
# Is specified to true but it seems it is not doing anything.

app.config["MAIL_SERVER"] = "am4.fcomet.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "info@viinum.com"
app.config["MAIL_PASSWORD"] = "ymqGWc;Na6m$"
app.config["MAIL_DEFAULT_SENDER"] = ("Gyllcare", "info@viinum.com")
app.config["MAIL_ASCII_ATTACHMENTS"] = False
# Standard configurations to connect to the mail server.

login_manager = LoginManager(app)
login_manager.login_view = "index"
db = SQLAlchemy(app)
mail = Mail(app)
schedule = BackgroundScheduler(daemon=True)
# Inititation of the login manager, SQLAlchemy database, mail functionality and the APS background scheduler.

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(30), unique=True)
    time = db.Column(db.String(30), unique=True)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(30), unique=True)
    time_on = db.Column(db.String(30), unique=False)
    time_off = db.Column(db.String(30), unique=False)

class LoginForm(FlaskForm):
    name = StringField("name")
    password = StringField("password")

class ScheduleForm(FlaskForm):
    list_of_choices = []
    for i in range(24):
        first = ""+str(i)+":00"
        second = ""+str(i)+":15"
        third = ""+str(i)+":30"
        fourth = ""+str(i)+":45"
        list_of_choices.append(first)
        list_of_choices.append(second)
        list_of_choices.append(third)
        list_of_choices.append(fourth)
    # Lines 74-83 generate a list that determines the choices for the selectfield.
    unit_co2_on = SelectField("CO2 schedule on", choices=list_of_choices)
    unit_co2_off = SelectField("CO2 schedule off", choices=list_of_choices)
    unit_o2_on = SelectField("O2 schedule on", choices=list_of_choices)
    unit_o2_off = SelectField("O2 schedule off", choices=list_of_choices)
    unit_light_on = SelectField("Light schedule on", choices=list_of_choices)
    unit_light_off = SelectField("Light schedule off", choices=list_of_choices)
    unit_temp_on = SelectField("Temp schedule on", choices=list_of_choices)
    unit_temp_off = SelectField("Temp schedule off", choices=list_of_choices)

app_start = Events.query.filter_by(id=1).first()
app_start.time = datetime.now().strftime("%d-%m-%Y %H:%M")
db.session.commit()
# Lines 94-96 store the date and time when the app is being initialised.

logfile = open("/home/pi/Desktop/logs/Gyllcare_log.txt", "a")
logfile.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " ###### Gyllcare has been initiated. \n")
logfile.close()
# Lines 99-101 log the date and time the app has been initialised in the Gyllcare_log.txt file.

unit_co2_time_on = Schedule.query.filter_by(id=1).first().time_on
unit_co2_time_off = Schedule.query.filter_by(id=1).first().time_off
unit_o2_time_on = Schedule.query.filter_by(id=2).first().time_on
unit_o2_time_off = Schedule.query.filter_by(id=2).first().time_off
unit_light_time_on = Schedule.query.filter_by(id=3).first().time_on
unit_light_time_off = Schedule.query.filter_by(id=3).first().time_off
unit_temp_time_on = Schedule.query.filter_by(id=4).first().time_on
unit_temp_time_off = Schedule.query.filter_by(id=4).first().time_off
# The currently stored values for the 'on'  and 'off' time for all modules are queried and stored in the respective variables.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# This decorator is used as part of the login functionality. It functions well but the workings are not clear.

@app.route("/", methods=["GET", "POST"])
def index():
    time = datetime.now().strftime(("%d/%m/%Y"))
    form = LoginForm()
    user = User.query.filter_by(username="JMKoelewijn").first() 
    # The user object being generated here is also part of the login functionality. It functions well but the workings are not exactly clear.
    if request.method == "POST":
        if form.validate_on_submit():
            if User.query.first().username == form.name.data and User.query.first().password == form.password.data:
                login_user(user)
                return redirect(url_for("gyllcare"))

    return render_template("login.html", form=form, time=time)

@app.route("/gyllcare", methods=["GET", "POST"]) # The main route is initiated.
@login_required
def gyllcare():

    schedule_form = ScheduleForm() # An object is initiated with respect to the ScheduleForm class.
    results = Events.query.filter_by(id=1).first() # The initiation time of the Gyllcare app is fetched from the Viinum database and stored locally.
    change_to_datetime = datetime.strptime(results.time, '%d-%m-%Y %H:%M') # The information is changed to a specific time format and stored locally.
    time_active = datetime.now().replace(microsecond=0) - change_to_datetime.replace(microsecond=0) # The difference in the current time and the initiation time is calculated and stored locally.
    gpio_14, gpio_15, gpio_18, gpio_23 = return_status() # The return_status() function returns a list from gpio_module.py which contains the current status of every GPIO pin.
    temperature = read_temp()
    time_span = x_data[-1]
    schedule_set = ""

    if request.method == "POST":

        # The "on" and "off" time values are retrieved from the form and are stored in the Viinum database for every unit.

        Schedule.query.filter_by(id=1).first().time_on = schedule_form.unit_co2_on.data
        Schedule.query.filter_by(id=1).first().time_off = schedule_form.unit_co2_off.data
        Schedule.query.filter_by(id=2).first().time_on = schedule_form.unit_o2_on.data
        Schedule.query.filter_by(id=2).first().time_off = schedule_form.unit_o2_off.data
        Schedule.query.filter_by(id=3).first().time_on = schedule_form.unit_light_on.data
        Schedule.query.filter_by(id=3).first().time_off = schedule_form.unit_light_off.data
        Schedule.query.filter_by(id=4).first().time_on = schedule_form.unit_temp_on.data
        Schedule.query.filter_by(id=4).first().time_off = schedule_form.unit_temp_off.data
        
        db.session.commit()

        schedule.reschedule_job("toggle_CO2_on", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_co2_on.data +':00')
        schedule.reschedule_job("toggle_CO2_off", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_co2_off.data +':00')
        schedule.reschedule_job("toggle_O2_on", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_o2_on.data +':00')
        schedule.reschedule_job("toggle_O2_off", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_o2_off.data +':00')
        schedule.reschedule_job("toggle_light_on", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_light_on.data +':00')
        schedule.reschedule_job("toggle_light_off", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_light_off.data +':00')
        schedule.reschedule_job("toggle_temp_on", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_temp_on.data +':00')
        schedule.reschedule_job("toggle_temp_off", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_temp_off.data +':00')

        schedule_set = "The new schedule has been initiated!"
    
    schedule_form.unit_co2_on.default = Schedule.query.filter_by(id=1).first().time_on
    schedule_form.unit_co2_off.default = Schedule.query.filter_by(id=1).first().time_off
    schedule_form.unit_o2_on.default = Schedule.query.filter_by(id=2).first().time_on
    schedule_form.unit_o2_off.default = Schedule.query.filter_by(id=2).first().time_off
    schedule_form.unit_light_on.default = Schedule.query.filter_by(id=3).first().time_on
    schedule_form.unit_light_off.default = Schedule.query.filter_by(id=3).first().time_off
    schedule_form.unit_temp_on.default = Schedule.query.filter_by(id=4).first().time_on
    schedule_form.unit_temp_off.default = Schedule.query.filter_by(id=4).first().time_off
    
    schedule_form.process()

    return render_template("gyllcare.html", gpio_14=gpio_14,
                                          gpio_15=gpio_15,
                                          gpio_18=gpio_18,
                                          gpio_23=gpio_23,
                                          time_active=time_active,
                                          schedule_form=schedule_form,
                                          schedule_set=schedule_set,
                                          temperature=temperature,
                                          time_span=time_span
                                          )
    
@app.route("/status", methods=["GET", "POST"])
@login_required
def status():
    gpio_14, gpio_15, gpio_18, gpio_23 = return_status()
    message = {'gpio_14_status':gpio_14,'gpio_15_status':gpio_15,'gpio_18_status':gpio_18,'gpio_23_status':gpio_23}
    
    if request.method == "POST":
        state = request.form['state']
        gpio = request.form['gpio']
        name = request.form['name']
        toggle(state, gpio, name)
    
    return jsonify(message)

@app.route("/email", methods=["POST"])
@login_required
def email():
    if request.method == "POST":

        schedulefile = open("/home/pi/Desktop/logs/Schedule_log.txt", "w")

        for i in schedule.get_jobs():
            schedulefile.write(str(i) + "\n")
        schedulefile.close()
 
        msg = Message("Gyllcare has send you a message", recipients=["mklwn@hotmail.com"])
        msg.body = "Attached you'll find the Gyllcare log files"

        with app.open_resource("/home/pi/Desktop/logs/Gyllcare_log.txt") as attach:
            msg.attach("Gyllcare_log.txt", "text/plain", attach.read())
        with app.open_resource("/home/pi/Desktop/logs/Schedule_log.txt") as attach_2:
            msg.attach("Schedule_log.txt", "text/plain", attach_2.read())
        
        mail.send(msg)
        
        return "200 OK"

@app.route("/shutdown", methods=["POST"])
@login_required
def shutdown():
    if request.method == "POST":
        command_1 = "sudo service apache2 stop"
        command_2 = "sudo shutdown -h now"
        subprocess.call(command_1.split())
        subprocess.call(command_2.split())
        # print("shutting down")
        return "200 OK"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

temperature_data = [25.0, 25.0, 25.0, 25.0]
x_data = [1, 2, 3, 4]

# temperature_data = []
# x_data = []

# def generate_list(): # For development
#     for i in range(23):
#         value = random()
#         scaled_value = 25 + (value * (30 - 25))
#         random_float = round(float(scaled_value), 1)
#         temperature_data.append(random_float)
#     return temperature_data

# def generate_xvalue():
#     for i in range(23):
#         x_data.append(i)
#     return x_data

# temperature_data = generate_list()
# x_data = generate_xvalue()

def read_temp_plot_data():

    plt.clf()

    x_data.append(x_data[-1] + 1)
    temperature_data.append(read_temp())

    if len(temperature_data) > 25:
        del temperature_data[0:-4]
        x_data.clear()
        x_data.extend([1, 2, 3, 4])

    max_temp = max(temperature_data)
    min_temp = min(temperature_data)

    x = np.array(x_data)
    y = np.array(temperature_data)

    # print(x)
    # print(y)

    bspline = make_interp_spline(x, y) 
    X_smooth = np.linspace(x.min(), x.max(), 500)
    Y_smooth = bspline (X_smooth)

    # print(X_smooth)
    # print(Y_smooth)
    # print(len(X_smooth))
    # print(len(Y_smooth))
  
    plt.tick_params(axis='both',
                    left=False, 
                    bottom=False, 
                    labelleft=False,
                    labelbottom=False)
    
    plt.ylim(min_temp - 2, max_temp + 2)

    plt.plot(X_smooth, Y_smooth, 
             marker='o', 
             markersize=30,
             markeredgewidth=0,
             markerfacecolor='#55efc4', 
             linestyle='--',
             color='#00b894', 
             linewidth=2, 
             markevery=[0, -1])
    
    plt.box(False)

    # i = 0
    # for el_y in Y_smooth:
    #     plt.annotate(str(el_y), (X_smooth[i], el_y), xytext=(-12, -4), xycoords="data", textcoords="offset pixels", color='white', fontweight=1000) if i % 50 == 0 else None
    #     i += 1

    plt.annotate(str(Y_smooth[0]), (X_smooth[0], Y_smooth[0]), xytext=(-12, -4), xycoords="data", textcoords="offset pixels", color='white', fontweight=1000)
    plt.annotate(str(Y_smooth[-1]), (X_smooth[-1], Y_smooth[-1]), xytext=(-12, -4), xycoords="data", textcoords="offset pixels", color='white', fontweight=1000)
    plt.text(1, min_temp - 2, f"Change in temperature since last {x_data[-1]} hours", color="#55efc4", fontsize="x-large")

    plt.savefig('/var/www/html/gyllcare/static/Resources/img/plot.svg', format="svg", bbox_inches='tight', pad_inches=0, transparent=True)
    # plt.savefig('/home/pi/Viinum/gyllcare/static/Resources/img/plot.svg', format="svg", bbox_inches='tight', pad_inches=0, transparent=True)
    
schedule.add_job(toggle_CO2_on,'interval', days=1, start_date='2021-05-01 ' + unit_co2_time_on +':00', id="toggle_CO2_on")
schedule.add_job(toggle_CO2_off,'interval', days=1, start_date='2021-05-01 ' + unit_co2_time_off +':00', id="toggle_CO2_off")
schedule.add_job(toggle_O2_on,'interval', days=1, start_date='2021-05-01 ' + unit_o2_time_on +':00', id="toggle_O2_on")
schedule.add_job(toggle_O2_off,'interval', days=1, start_date='2021-05-01 ' + unit_o2_time_off +':00', id="toggle_O2_off")
schedule.add_job(toggle_light_on,'interval', days=1, start_date='2021-05-01 ' + unit_light_time_on +':00', id="toggle_light_on")
schedule.add_job(toggle_light_off,'interval', days=1, start_date='2021-05-01 ' + unit_light_time_off +':00', id="toggle_light_off")
schedule.add_job(toggle_temp_on,'interval', days=1, start_date='2021-05-01 ' + unit_temp_time_on +':00', id="toggle_temp_on")
schedule.add_job(toggle_temp_off,'interval', days=1, start_date='2021-05-01 ' + unit_temp_time_off +':00', id="toggle_temp_off")
schedule.add_job(read_temp_plot_data,'interval', minutes=60, start_date='2021-05-01 00:00:00', id="read_temp_plot_data")

schedule.start()

if __name__ == "__main__":
    app.run(debug=True)
