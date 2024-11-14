import matplotlib.pyplot as plt
from utilities import FileReader
import numpy as np

def plot_ground_truth(ax):
    # Parameters
    dt = 0.1  # Time step
    total_time = 15  # Total simulation time
    linear_velocity = 0.0
    angular_velocity = 1.0
    max_linear_velocity = 1.0

    # Initialize position and orientation
    x, y, theta = 0.0, 0.0, 0.0

    # Lists to store the path
    x_path = [x]
    y_path = [y]

    # Simulate the motion
    for t in np.arange(0, total_time, dt):
        linear_velocity += 0.01 if linear_velocity < max_linear_velocity else 0.0
        x += linear_velocity * np.cos(theta) * dt
        y += linear_velocity * np.sin(theta) * dt
        theta += angular_velocity * dt

        x_path.append(x)
        y_path.append(y)

    # Plot the path
    ax.plot(x_path, y_path, label="ground truth")


def plot_errors(filename):
    
    headers, values=FileReader(filename).read_file()
    
    time_list=[]
    
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    
    
    fig, axes = plt.subplots(2,1, figsize=(14,6))


    axes[0].plot([lin[len(headers) - 3] for lin in values], [lin[len(headers) - 2] for lin in values], label="kalman filter")
    plot_ground_truth(axes[0])
    axes[0].set_title("state space")
    axes[0].grid()
    axes[0].legend()
    axes[0].axis('equal')

    
    axes[1].set_title("each individual state")
    for i in range(0, len(headers) - 1):
        axes[1].plot(time_list, [lin[i] for lin in values], label= headers[i])

    axes[1].legend()
    axes[1].grid()

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


