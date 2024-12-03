import matplotlib.pyplot as plt
from utilities import FileReader
import numpy as np

def read_pgm(filename, x_offset=-60, y_offset=0):
    with open(filename, 'rb') as f:
        # Check if it's a PGM file
        header = f.readline().decode().strip()

        if header != 'P5':
            raise ValueError('Invalid PGM file format')

        # Skip comments
        line = f.readline().decode().strip()
        while line.startswith('#'):
            line = f.readline().decode().strip()

        # Read width, height, and maximum gray value
        width, height = map(int, line.split())

        # Read the image data
        image_data = np.frombuffer(f.read(), dtype=np.uint8).reshape((height, width))

    return image_data

def plot_pgm_image():
    # Convert pixel values to a NumPy array
    image_array = read_pgm("cropped_room.pgm")

    # Plot the image
    plt.imshow(image_array, cmap='gray')

def plot_errors():
    headers, values=FileReader("robotPoseGoal1Euc.csv").read_file()

    # MAP RESOLUTION
    resolution = 0.05

    # Offset for the origin
    x_off = 11
    y_off = 74

    # Scale and shift the values
    ekf_y = [-lin[7] / resolution + y_off for lin in values]
    ekf_x = [lin[6] / resolution + x_off  for lin in values]
    raw_y = [-lin[9] / resolution + y_off for lin in values]
    raw_x = [lin[8] / resolution + x_off for lin in values]

    # indicate the start and end positions of each plot
    plt.scatter(ekf_x[0], ekf_y[0], c='b', label="Euclidian EKF Start", marker='s', alpha=0.75)
    plt.scatter(ekf_x[-1], ekf_y[-1], c='b', label="Euclidian EKF End")
    plt.scatter(raw_x[0], raw_y[0], c='orange', label="Euclidian Raw Sensor Start", marker='s', alpha=0.75)
    plt.scatter(raw_x[-1], raw_y[-1], c='orange', label="Euclidian Raw Sensor End")

    # plot robot trajectories
    plt.plot(ekf_x, ekf_y, label="Euclidian EKF Localization")
    plt.plot(raw_x, raw_y, label="Euclidian Raw Sensor Localization")

    headers, values=FileReader("robotPoseGoal1Man.csv").read_file()

    # Scale and shift the values
    ekf_y = [-lin[7] / resolution + y_off for lin in values]
    ekf_x = [lin[6] / resolution + x_off  for lin in values]
    raw_y = [-lin[9] / resolution + y_off for lin in values]
    raw_x = [lin[8] / resolution + x_off for lin in values]

    # indicate the start and end positions of each plot
    plt.scatter(ekf_x[0], ekf_y[0], c='g', label="Manhattan EKF Start", marker='s', alpha=0.75)
    plt.scatter(ekf_x[-1], ekf_y[-1], c='g', label="Manhattan EKF End")
    plt.scatter(raw_x[0], raw_y[0], c='red', label="Manhattan Raw Sensor Start", marker='s', alpha=0.75)
    plt.scatter(raw_x[-1], raw_y[-1], c='red', label="Manhattan Raw Sensor End")

    # plot robot trajectories
    plt.plot(ekf_x, ekf_y, label="Manhattan EKF Localization")
    plt.plot(raw_x, raw_y, label="Manhattan Raw Sensor Localization")

    # Adjust x-axis tick labels to origin
    x_ticks = ax.get_xticks()
    x_labels = [f"{tick - x_off:.1f}" for tick in x_ticks]
    ax.set_xticklabels(x_labels)

    # Adjust y-axis tick labels to origin
    y_ticks = ax.get_yticks()
    y_labels = [f"{-(tick - y_off):.1f}" for tick in y_ticks]
    ax.set_yticklabels(y_labels)

if __name__=="__main__":
    fix, ax = plt.subplots()

    # change fig size
    fix.set_size_inches(8, 4)

    plot_pgm_image()
    plot_errors()

    plt.title('Goal Pose 1 - Euclidian vs Manhattan Heuristic')

    # move the legend outside of the plot
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # adjustments to make plot look better
    plt.subplots_adjust(right=0.6)
    plt.subplots_adjust(left=0.1)
    plt.grid()

    plt.xlabel('X Position (scaled to map resolution)')
    plt.ylabel('Y Position (scaled to map resolution)')

    plt.show()