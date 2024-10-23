import matplotlib.pyplot as plt
from utilities import FileReader
import numpy as np


def parabola_trajectory_planner():
    trajectory_points = []
    x_values = np.linspace(-2, -0.5, num=15)
    y_values = []

    # Robot in sim starts off at these coordinates so it was required
    starting_x = -2 # set to 0 for real
    starting_y = -0.5 # set to 0 for real

    for x in x_values:
        y = ((x - starting_x) ** 2) + starting_y
        y_values.append(y)
    return x_values, y_values

def sigmoid_trajectory_planner():
    y_values = []
    x_values = np.linspace(-2, 0.5, num=25)

    # Robot in sim starts off at these coordinates so it was required
    starting_x = -2 # set to 0 for real
    starting_y = -0.5 # set to 0 for real

    for x in x_values:
        y = 2 / (1 + np.exp(-2 * (x-starting_x))) - 1 + starting_y
        y_values.append(y)
    return x_values, y_values

def plot_errors(filename):
    
    headers, values=FileReader(filename).read_file()
    
    time_list=[]
    
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    if filename == 'robot_pose.csv':
        axes[0].plot([lin[0] for lin in values], [lin[1] for lin in values])
        axes[0].set_title("state space")
        axes[0].grid()
        axes[0].axis('equal')

        # Plot the target trajectory for parabola
        # x_values, y_values = parabola_trajectory_planner()
        x_values, y_values = sigmoid_trajectory_planner()

        axes[0].plot(x_values, y_values, marker='o')

    if filename == 'angular.csv':
        axes[1].set_title("each individual state")
        for i in range(0, len(headers) - 1):
            axes[1].plot(time_list, [lin[i] for lin in values], label= headers[i]+ " angular")

        axes[1].legend()
        axes[1].grid()

    if filename == 'linear.csv':
        axes[2].set_title("each individual state")
        for i in range(0, len(headers) - 1):
            axes[2].plot(time_list, [lin[i] for lin in values], label=headers[i] + " linear")

        axes[2].legend()
        axes[2].grid()

import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for filename in filenames:
        plot_errors(filename)

    plt.show()


