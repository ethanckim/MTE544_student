import matplotlib.pyplot as plt
from utilities import FileReader

# This function does the plotting for the trajectory planner
def plot_errors(filename):
    
    headers, values=FileReader(filename).read_file()
    
    time_list=[]
    
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append((val[-1] - first_stamp) / 1e9)

    if filename == 'robot_pose.csv':
        axes[0, 0].plot([lin[0] for lin in values], [lin[1] for lin in values])
        axes[0, 0].set_title("2D Trajectory Top View")
        axes[0, 0].grid()
        axes[0, 0].set_xlabel('X Position (m)')
        axes[0, 0].set_ylabel('Y Position (m)')
        axes[0, 0].axis('equal')

        for i in range(0, len(headers) - 1):
            axes[0, 1].plot(time_list, [lin[i] for lin in values])

        axes[0, 1].set_title("Robot Pose vs Time")
        axes[0, 1].set_xlabel('Time (s)')
        axes[0, 1].set_ylabel('Pose Value')
        axes[0, 1].legend(['X (m)', 'Y (m)', 'θ (rad)'])
        axes[0, 1].grid()

    if filename == 'angular.csv':
        axes[1, 0].plot([lin[0] for lin in values], [lin[1] for lin in values], label='Angular (rad)')

        for i in range(0, len(headers) - 2):
            axes[1, 1].plot(time_list, [lin[i] for lin in values])

    if filename == 'linear.csv':
        axes[1, 0].plot([lin[0] for lin in values], [lin[1] for lin in values], label = 'Linear (m)')

        for i in range(0, len(headers) - 2):
            axes[1, 1].plot(time_list, [lin[i] for lin in values])

    axes[1, 0].set_title("Error vs Derivative Error")
    axes[1, 0].grid()
    axes[1, 0].set_xlabel('Error')
    axes[1, 0].set_ylabel('Derivative Error')
    axes[1, 0].legend()

    axes[1, 1].set_title("Error and Derivative Error vs Time")
    axes[1, 1].set_xlabel('Time (s)')
    axes[1, 1].set_ylabel('Error / Error Derivative')
    axes[1, 1].grid()
    axes[1, 1].legend(['Angular Error (rad)', 'Angular Error Derivative (rad/s)', 'Linear Error (m)', 'Linear Error Derivative (m/s)'])

import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files

    _, axes = plt.subplots(2, 2, figsize=(10, 9))

    for filename in filenames:
        plot_errors(filename)

    # plt.suptitle('Plots for Point Planner (P Controller)')
    plt.suptitle('Plots for Point Planner (PID Controller)')
    plt.tight_layout()
    plt.show()



