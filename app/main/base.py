from .gpio import ToggleSwitch, alarm_on

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

from apscheduler.schedulers.background import BackgroundScheduler
import threading

class AlarmMode():       
    def start(self):
        AlarmMode.stop_thread = False
        self.id = threading.Thread(target=alarm_on, args=(lambda : AlarmMode.stop_thread,))
        self.id.start()
    
    def stop(self):
        AlarmMode.stop_thread = True
        self.id.join()

CO2 = ToggleSwitch(14, "CO2")
O2 = ToggleSwitch(15, "O2")
Light = ToggleSwitch(18, "Light")
Therm = ToggleSwitch(23, "Therm")
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
    plt.text(1, min_temp - 2, f"Change in temperature since last {x_data[-1]} hours", color="#ffffff", fontsize="x-large")

    plt.savefig('/var/www/html/gyllcare/static/Resources/img/plot.svg', format="svg", bbox_inches='tight', pad_inches=0, transparent=True)