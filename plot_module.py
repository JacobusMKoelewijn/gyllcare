import matplotlib
matplotlib.use('Agg') # What does this do exactly? Needed after "RuntimeError: main thread is not in main loop. Related to Tkinter?"
import matplotlib.pyplot as plt
# from pathlib import Path

# Had to install sudo apt install libatlas-base-dev to surpress a warning

def plot_graph():
    plt.clf()
    with open("/home/pi/Desktop/logs/Temperature_log.txt") as tempfile:
        data = [float(line.strip()) for line in tempfile.readlines()]
    plt.title("Temperature progress of the past 3 days", color="#00a8ff", fontsize="xx-large", pad=12.0)
    plt.ylabel('Temperature [\u00B0C]', color="#00a8ff", fontsize="xx-large", labelpad=10)
    plt.grid(which='both', color="lightgrey")
    # plt.xlabel('<< the past 3 days >>', color="#00a8ff", fontsize="xx-large", labelpad=10)
    plt.tick_params(axis='y', direction='out', length=6, width=1, labelsize="15")
    plt.tick_params(axis='x', bottom=False, labelbottom=False)
    plt.ylim((24, 34))
    plt.plot(data, '#00a8ff', linewidth=3)
    # plt.savefig('static/Resources/img/plot.svg', format="svg", transparent=True)
    plt.savefig('/var/www/html/aquapi/static/Resources/img/plot.svg', format="svg", transparent=True)
    # print("refreshed")
