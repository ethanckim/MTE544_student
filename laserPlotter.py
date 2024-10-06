# laserPlotter.py takes in a LaserScan message log file (.csv), generated by motions.py.
# The ranges and angle_increment in the first message (first row) of the file
# is used to plot the scanned data points in a 2D x-y coordinate grid.

import matplotlib.pyplot as plt
from utilities import FileReader
import numpy as np
import math

def plot_laser(filename):
    headers, values=FileReader(filename).read_file()

    # Choose an arbitrary row index to plot (we are only asked to plot one scan)
    row_index = 20

    # Get the angle increment
    ang_increment = values[row_index][-2]

    # Start plotting from theta = 0
    theta = 0

    # Initialize lists to hold x and y data for each point
    x = []
    y = []

    for i in range(0, len(values[row_index])-2):
        # Get radius of point
        r = float(values[row_index][i])

        # Skip inf or NaN values but still increment theta
        if math.isinf(r) or math.isnan(r):
            theta += ang_increment
            continue

        # Convert polar coordinates to cartesian and append to appropriate list
        x.append(values[row_index][i] * np.cos(theta))
        y.append(values[row_index][i] * np.sin(theta))

        # Increment theta by the angle increment
        theta += ang_increment

    # Plot the data with relevant title, labels, legend, etc.
    plt.scatter(x, y, label= "2D Top View Trajectory (x vs y)")
    plt.legend()
    plt.title("Cartesian Pose Data from Single Laser Scan")
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
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
        plot_laser(filename)