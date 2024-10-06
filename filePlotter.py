# You can use this file to plot the logged sensor data
# Note that you need to modify/adapt it to your own files
# Feel free to make any modifications/additions here

import matplotlib.pyplot as plt
from utilities import FileReader

def plot_errors(filename):
    
    headers, values=FileReader(filename).read_file() 
    time_list=[]
    first_stamp=values[0][-1]
    
    for val in values:
        time_val = val[-1] - first_stamp
        # convert time_val from ns to s
        time_list.append(time_val/1e9)

    for i in range(0, len(headers) - 1):
        # skip the degree data for plotting
        if headers[i] == "th_deg":
            continue
        plt.plot(time_list, [lin[i] for lin in values])

    # Uncomment the relevant lines to plot the data for the specific motion - labels, titles
    plt.legend(["X Acceleration [m/s^2]", "Y Acceleration [m/s^2]", 'Angular Velocity [rad/s]'])
    # plt.legend(["X Position [m]", "Y Position [m]", 'Orientation [rad]'])
    # plt.title("IMU Data for Circular Motion")
    # plt.title("IMU Data for Spiral Motion")
    plt.title("IMU Data for Straight Line Motion")
    # plt.title("ODOM Data for Circular Motion")
    # plt.title("ODOM Data for Spiral Motion")
    # plt.title("ODOM Data for Straight Line Motion")
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (X, Y), Velocity (θ)")
    # plt.ylabel("Position")
    plt.grid()
    plt.show()
    
import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files
    for filename in filenames:
        plot_errors(filename)
