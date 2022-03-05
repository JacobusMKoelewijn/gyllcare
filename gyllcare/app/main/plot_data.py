import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from datetime import datetime, timedelta
import pickle

from gyllcare.config import IN_PRODUCTION
from gyllcare.config import ROOT_DIR


from gyllcare import create_logger

log = create_logger(__name__)

if IN_PRODUCTION:
    from .temp import read_temp
    from .pH import read_pH
else:
    def read_temp():
        return(40)

    def read_pH(cmd):
        return(5.0)


time_data = [i for i in pd.date_range((datetime.now().replace(microsecond=0, second=0, minute=0) - timedelta(hours=47)), periods=48, freq="H")]
pH_data = pickle.load(open(ROOT_DIR + '/data/saved_pH_data', 'rb'))
temperature_data = pickle.load(open(ROOT_DIR + '/data/saved_temperature_data', 'rb'))


def read_temp_pH_plot_data():
    """
    Create a graph with the desired layout using the temperature and pH data over 48 hours.
    """

    plt.clf()

    time_data.append(datetime.now().replace(microsecond=0, second=0))
    pH_data.append(read_pH("R"))
    temperature_data.append(read_temp())

    del time_data[0]
    del pH_data[0]
    del temperature_data[0]

    pickle.dump(pH_data, open(ROOT_DIR + '/data/saved_pH_data', 'wb'))
    pickle.dump(temperature_data, open(ROOT_DIR + '/data/saved_temperature_data', 'wb'))

    log.info(time_data, len(time_data))
    log.info(pH_data, len(pH_data))
    log.info(temperature_data, len(temperature_data))

    zipped = list(zip(time_data, temperature_data, pH_data))

    df = pd.DataFrame(zipped, columns=['Time', 'Temperature', 'pH'])
    df = df.set_index('Time')

    max_temp = df["Temperature"].max()
    min_temp = df["Temperature"].min()
    max_pH = df["pH"].max()
    min_pH = df["pH"].min()
    
    log.info(df)
    resampled_df = df.resample('T').asfreq()
    log.info(resampled_df)
    smooth_df = resampled_df.interpolate(method='cubic')
    log.info(smooth_df)
   
    ax = smooth_df.plot(figsize = (12, 8), secondary_y='pH', legend=False, style={'Temperature':'#DD7373', 'pH':'#63ADF2'}, fontsize="21", linewidth=5)
    ax.set_ylabel("Temperature ($^{o}$C)", color="#DD7373", fontsize="25", labelpad=15)
    ax.right_ax.set_ylabel("pH", color="#63ADF2", fontsize="25", rotation="270", labelpad=35)
    ax.set_xlabel("")
    ax.tick_params(axis='y', colors='#DD7373', width=3, length=10)
    ax.tick_params(axis='x', which='minor', colors='#ffffff', width=3, length=10)
    ax.tick_params(axis='x', which='major', colors='#55efc4', width=3, length=16)
    ax.right_ax.tick_params(axis='y', colors="#63ADF2", width=3, length=10)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_ylim([min_temp - 3, max_temp + 3])
    ax.right_ax.set_ylim([min_pH - 1, max_pH + 1])

    plt.xticks(fontsize="20")
    plt.box(False)
    plt.savefig(ROOT_DIR + '/app/static/Resources/img/plot.svg', format="svg", bbox_inches='tight', pad_inches=0, transparent=True)