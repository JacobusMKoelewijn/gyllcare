import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from datetime import datetime, timedelta

import random

from app.config import IN_PRODUCTION

# also need temperature corrected!

if IN_PRODUCTION:
    from .temp import read_temp
    from .pH import read_pH
else:
    def read_temp():
        return(40)

    def read_pH():
        return(6)

# Dummy data
# time_data = [i for i in pd.date_range((datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d"), periods=48, freq="H")]
# pH_data = [4, 5, 6, 5, 8, 5, 8, 7, 4, 7, 4, 5, 7, 5, 4, 6, 4, 4, 7, 4, 6, 6, 8, 5, 4, 7, 4, 7, 5, 4, 4, 4, 5, 7, 4, 8, 7, 7, 8, 6, 8, 6, 6, 5, 5, 4, 4, 4]
# temperature_data = [31, 35, 27, 29, 25, 34, 32, 35, 31, 29, 32, 27, 35, 26, 26, 26, 27, 26, 25, 34, 27, 26, 28, 28, 25, 33, 33, 29, 27, 29, 32, 28, 32, 27, 32, 28, 31, 25, 34, 34, 30, 26, 29, 26, 28, 35, 33, 33]

# Less data
# time_data = [i for i in pd.date_range((datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d"), periods=40, freq="H")]
# pH_data = [4, 5, 6, 5, 8, 5, 8, 7, 4, 7, 4, 5, 7, 5, 4, 6, 4, 4, 7, 4, 6, 6, 8, 5, 4, 7, 4, 7, 5, 4, 4, 4, 5, 7, 4, 8, 7, 7, 8, 6]
# temperature_data = [31, 35, 27, 29, 25, 34, 32, 35, 31, 29, 32, 27, 35, 26, 26, 26, 27, 26, 25, 34, 27, 26, 28, 28, 25, 33, 33, 29, 27, 29, 32, 28, 32, 27, 32, 28, 31, 25, 34, 34]

time_data = [i for i in pd.date_range((datetime.today() - timedelta(hours=10)).strftime("%Y-%m-%d"), periods=6, freq="H")]
pH_data = [7, 7, 7, 7, 7, 7]
temperature_data = [30, 30, 30, 30, 30, 30]


def read_temp_pH_plot_data():
    """
    To be added
    """

    plt.clf()

    # time_data.append(datetime.fromisoformat("2022-02-14 17:00:00"))
    
    time_data.append(datetime.now())
    pH_data.append(read_pH("R"))
    temperature_data.append(read_temp())

    print(time_data)
    print(pH_data)
    print(temperature_data)

    zipped = list(zip(time_data, temperature_data, pH_data))


    df = pd.DataFrame(zipped, columns=['Time', 'Temperature', 'pH'])
    df = df.set_index('Time')
    
    print(df)

    if len(df) > 6:
        df = df.iloc[1: , :]
    
    print(df)

    resampled_df = df.resample('T').asfreq()
    
    print(resampled_df)
    smooth_df = resampled_df.interpolate(method='cubic')
    print(smooth_df)

   
    ax = smooth_df.plot(figsize = (12, 8), secondary_y='pH', legend=False, style={'Temperature':'#DD7373', 'pH':'#63ADF2'}, fontsize="21", linewidth=5)
    ax.set_xlabel("")
    ax.tick_params(axis='y', colors='#DD7373', width=3, length=10)
    ax.tick_params(axis='x', which='minor', colors='#ffffff', width=3, length=10)
    ax.tick_params(axis='x', which='major', colors='#55efc4', width=3, length=16)
    ax.right_ax.tick_params(axis='y', colors="#63ADF2", width=3, length=10)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.margins(0.2)
    ax.right_ax.margins(0.2)

    plt.xticks(fontsize="20")
    plt.box(False)

    if IN_PRODUCTION:
        plt.savefig('/var/www/html/gyllcare/app/static/Resources/img/plot.svg', format="svg", bbox_inches='tight', pad_inches=0, transparent=True)
    else:
        plt.savefig('/home/pi/Viinum/gyllcare/app/static/Resources/img/plot.svg', format="svg", bbox_inches='tight', pad_inches=0, transparent=True)

# read_temp_pH_plot_data()