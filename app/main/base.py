from .gpio import ToggleSwitch, alarm_on, return_status
from .temp import read_temp
from .models import Schedule
from .extensions import db
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

from apscheduler.schedulers.background import BackgroundScheduler
import threading

# from gyllcare import create_app
# app = create_app()

class AlarmMode():      
    def start(self):
        AlarmMode.stop_thread = False
        self.id = threading.Thread(target=alarm_on, args=(lambda : AlarmMode.stop_thread,))
        self.id.start()
    
    def stop(self):
        AlarmMode.stop_thread = True
        self.id.join()


class Scheduler():
    def __init__(self, id, schedule_id):
        self.id = id
        self.schedule_id = schedule_id
    
    
    def return_status(self):
        self.state = Schedule.query.filter_by(id=self.id).first().active
        return self.state

    def pause_schedule(self):
        schedule.pause_job(job_id=self.schedule_id + '_on')
        schedule.pause_job(job_id=self.schedule_id + '_off')
        print("paused")

        # schedule.reschedule_job("CO2.switch_on", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_co2_on.data +':00')
        # schedule.reschedule_job("CO2.switch_off", trigger="interval", days=1, start_date='2020-12-10 ' + schedule_form.unit_co2_off.data +':00')
    
    def resume_schedule(self):
        schedule.resume_job(job_id=self.schedule_id + '_on')
        schedule.resume_job(job_id=self.schedule_id + '_off')
        print("resumed")

    def toggle_state(self):

        status = self.return_status()

        if(status):
            Schedule.query.filter_by(id=self.id).first().active = False
            self.pause_schedule()
        else:
            Schedule.query.filter_by(id=self.id).first().active = True
            self.resume_schedule()
        
        db.session.commit()

CO2 = ToggleSwitch(25, "CO2")
O2 = ToggleSwitch(8, "O2")
Light = ToggleSwitch(7, "Light")
Therm = ToggleSwitch(1, "Therm")

CO2_scheduler = Scheduler(1, "toggle_CO2")
O2_scheduler = Scheduler(2, "toggle_O2")
Light_scheduler = Scheduler(3, "toggle_light")
Therm_scheduler = Scheduler(4, "toggle_temp")

alarm = AlarmMode()
schedule = BackgroundScheduler(daemon=True)

# Dummy data
temperature_data = [25.0, 25.0, 25.0, 25.0]
x_data = [1, 2, 3, 4]

matplotlib.use('Agg')

def read_temp_plot_data():

    plt.clf()

    x_data.append(x_data[-1] + 1)
    temperature_data.append(read_temp())

    if len(temperature_data) > 48:
        del temperature_data[0:-4]
        x_data.clear()
        x_data.extend([1, 2, 3, 4])

    max_temp = max(temperature_data)
    min_temp = min(temperature_data)

    x = np.array(x_data)
    y = np.array(temperature_data)


    bspline = make_interp_spline(x, y) 
    X_smooth = np.linspace(x.min(), x.max(), 500)
    Y_smooth = bspline (X_smooth)
  
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
            #  color='#00b894',
             color='#ffffff',
             linewidth=2, 
             markevery=[0, -1])
    
    plt.box(False)

    plt.annotate(str(Y_smooth[0]), (X_smooth[0], Y_smooth[0]), xytext=(-12, -4), xycoords="data", textcoords="offset pixels", color='white', fontweight=1000)
    plt.annotate(str(Y_smooth[-1]), (X_smooth[-1], Y_smooth[-1]), xytext=(-12, -4), xycoords="data", textcoords="offset pixels", color='white', fontweight=1000)
    plt.text(1, min_temp - 2, f"Change in water temperature since last {x_data[-1]} hours.", color="#ffffff", fontsize="x-large")

    plt.savefig('/var/www/html/gyllcare/app/static/Resources/img/plot.svg', format="svg", bbox_inches='tight', pad_inches=0, transparent=True)