import matplotlib.pyplot as plt
from utilities import FileReader
import numpy as np


def parabola_trajectory_planner():
    # Robot in sim starts off at these coordinates so it was required
    starting_x = 0 # set to 0 for real
    starting_y = 0 # set to 0 for real

    x_values = np.linspace(0 + starting_x, 1.5 + starting_y, num=15)
    y_values = []

    for x in x_values:
        y = ((x - starting_x) ** 2) + starting_y
        y_values.append(y)
    return x_values, y_values

def sigmoid_trajectory_planner():
    # Robot in sim starts off at these coordinates so it was required
    starting_x = 0 # set to 0 for real
    starting_y = 0 # set to 0 for real

    y_values = []
    x_values = np.linspace(0 + starting_x, 2.5 + starting_y, num=25)

    for x in x_values:
        y = 2 / (1 + np.exp(-2 * (x-starting_x))) - 1 + starting_y
        y_values.append(y)
    return x_values, y_values

def plot_errors(filename):
    
    headers, values=FileReader(filename).read_file()
    
    time_list=[]
    
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append((val[-1] - first_stamp) / 1e9)

    if filename == 'robot_pose.csv':
        axes[0,].plot([lin[0] for lin in values], [lin[1] for lin in values], label='Robot Trajectory')
        axes[0].set_title("2D Trajectory Top View")
        axes[0].grid()
        axes[0].set_xlabel('X Position (m)')
        axes[0].set_ylabel('Y Position (m)')
        axes[0].axis('equal')


        # Plot the target trajectory for parabola
        # x_values, y_values = parabola_trajectory_planner()
        x_values, y_values = sigmoid_trajectory_planner()

        axes[0].scatter(x_values, y_values, color='r', s=15, alpha=0.6, label='Goal Points')
        axes[0].legend()

    if filename == 'angular.csv':

        for i in range(0, len(headers) - 3):
            axes[1].plot(time_list, [lin[i] for lin in values])

    if filename == 'linear.csv':

        for i in range(0, len(headers) - 3):
            axes[1].plot(time_list, [lin[i] for lin in values])

    axes[1].set_title("Error vs Time")
    axes[1].set_xlabel('Time (s)')
    axes[1].set_ylabel('Error')
    axes[1].grid()
    axes[1].legend(['Angular Error (rad)', 'Linear Error (m)'])

import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files

    _, axes = plt.subplots(1, 2, figsize=(10, 5))

    for filename in filenames:
        plot_errors(filename)

    # plt.suptitle('Plots for Trajectory Planner (Parabola)')
    plt.suptitle('Plots for Trajectory Planner (Sigmoid)')
    plt.tight_layout()
    plt.show()



