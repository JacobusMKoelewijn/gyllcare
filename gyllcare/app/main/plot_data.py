import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from datetime import datetime, timedelta
import pickle

import random

from gyllcare.config import IN_PRODUCTION
from gyllcare.config import ROOT_DIR

# also need temperature corrected!

if IN_PRODUCTION:
    from .temp import read_temp
    from .pH import read_pH
else:
    def read_temp():
        return(30)

    def read_pH(cmd):
        return(6.000)


time_data = [i for i in pd.date_range((datetime.now().replace(microsecond=0, second=0, minute=0) - timedelta(hours=47)), periods=48, freq="H")]
pH_data = pickle.load(open(ROOT_DIR + '/saved_pH_data', 'rb'))
temperature_data = pickle.load(open(ROOT_DIR + '/saved_temperature_data', 'rb'))
# print('succes')
# print(len(time_data))
# print(pH_data, len(pH_data))
# print(temperature_data, len(temperature_data))

# pH_data = [1, 1, 1]
# temperature_data = [2, 2, 2]

def read_temp_pH_plot_data():
    """
    To be added
    """

    plt.clf()

    # time_data.append(datetime.fromisoformat("2022-02-14 17:00:00"))
    # Refactor later

    time_data.append(datetime.now().replace(microsecond=0, second=0))
    pH_data.append(read_pH("R"))
    temperature_data.append(read_temp())

    del time_data[0]
    del pH_data[0]
    del temperature_data[0]



    pickle.dump(pH_data, open(ROOT_DIR + '/main/saved_pH_data', 'wb'))
    pickle.dump(temperature_data, open(ROOT_DIR + '/main/saved_temperature_data', 'wb'))

    print(time_data, len(time_data))
    print(pH_data, len(pH_data))
    print(temperature_data, len(temperature_data))

    zipped = list(zip(time_data, temperature_data, pH_data))


    df = pd.DataFrame(zipped, columns=['Time', 'Temperature', 'pH'])
    df = df.set_index('Time')

    # max_time = df.index.max()
    # min_time = df.index.min()
    max_temp = df["Temperature"].max()
    min_temp = df["Temperature"].min()
    max_pH = df["pH"].max()
    min_pH = df["pH"].min()
    
    print(df)

    # if len(df) > 6:
        # df = df.iloc[1: , :]
        # del time_data[0]
        # del pH_data[0]
        # del temperature_data[0]
    
    # print(df)

    # save df to pickle.

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

    # ax.margins(0.2)
    # ax.right_ax.margins(0.2)
    # ax.margins(x=1000)
    # ax.set_xlim([min_time - 5, max_time + 5])
    ax.set_ylim([min_temp - 5, max_temp + 5])
    ax.right_ax.set_ylim([min_pH - 3, max_pH + 3])

    plt.xticks(fontsize="20")
    plt.box(False)

    # if IN_PRODUCTION:
        # plt.savefig('/var/www/html/gyllcare/app/static/Resources/img/plot.svg', format="svg", bbox_inches='tight', pad_inches=0, transparent=True)
    # else:
        # plt.savefig('/home/pi/Viinum/gyllcare/app/static/Resources/img/plot.svg', format="svg", bbox_inches='tight', pad_inches=0, transparent=True)
    
    plt.savefig(ROOT_DIR + '/static/Resources/img/plot.svg', format="svg", bbox_inches='tight', pad_inches=0, transparent=True)

# read_temp_pH_plot_data()