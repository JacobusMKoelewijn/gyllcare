import matplotlib
matplotlib.use('Agg') # What does this do exactly? Needed after "RuntimeError: main thread is not in main loop. Related to Tkinter?"
import matplotlib.pyplot as plt
import numpy as np
# Had to install sudo apt install libatlas-base-dev to surpress a warning

def plot_graph():
    plt.clf() # Clears the current figure
    with open("/home/pi/Desktop/logs/Temperature_log.txt") as tempfile:
        data = [float(line.strip()) for line in tempfile.readlines()]
        # last_data_input = tempfile.read(len(data))
        # before_last_data_input = tempfile.read(len(data) - 1)
        # print(last_data_input)
        # print(before_last_data_input)
        # if len(data) > 5:
            # workaround = open("/home/pi/Desktop/logs/Temperature_log.txt", "a")
            # tempfile.truncate(0)
            # tempfile.write("25 \n")
            # tempfile.write("26 \n")
        #     workaround.write(last_data_input + "\n")
        #     workaround.close()
  
    min_max = np.loadtxt("/home/pi/Desktop/logs/Temperature_log.txt")
    # print(len(data))
    # plt.title("Temperature progress of the past 3 days", color="#00a8ff", fontsize="xx-large", pad=12.0)
    # plt.ylabel('Temperature [\u00B0C]', color="#00b894", fontsize="xx-large", labelpad=10)
    # plt.grid(which='both', color="lightgrey")
    # plt.xlabel('<< the past 3 days >>', color="#00a8ff", fontsize="xx-large", labelpad=10)
    plt.tick_params(axis='both',
                    colors="#00b894", 
                    left=True, 
                    bottom=False, 
                    labelleft=True,
                    labelbottom=False)
    # plt.tick_params(axis='x', bottom=False, labelbottom=False)
    plt.ylim((np.amin(min_max) - 1, np.amax(min_max) + 1))
    plt.plot(data, 
             marker='o', 
             markersize=10,
            #  markeredgewidth=2,
             markerfacecolor='#55efc4', 
             linestyle='--', 
             color='#00b894', 
             linewidth=1, 
             markevery=5)
    

    # plt.text(4, data[4], str(data[4]), fontsize=12, color="#00b894")
    
    plt.box(False)
    # plt.savefig('static/Resources/img/plot.svg', format="svg", transparent=True)
    # plt.savefig('/var/www/html/gyllcare/static/Resources/img/plot.svg', format="svg", transparent=True)
    plt.savefig('/home/pi/Viinum/gyllcare/static/Resources/img/plot.svg', format="svg", bbox_inches='tight', pad_inches=0, transparent=True)
    
    # print("refreshed")
    # print(data)
