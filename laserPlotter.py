import matplotlib.pyplot as plt
from utilities import FileReader
import numpy as np
import math

def plot_laser(filename):
    headers, values=FileReader(filename).read_file() 

    ang_increment = values[0][-2]
    theta = 0
    x = []
    y = []

    for i in range(0, len(values[0])-2):
        r = float(values[0][i])

        if math.isinf(r) or math.isnan(r):
            theta += ang_increment
            continue

        x.append(values[0][i] * np.cos(theta))
        y.append(values[0][i] * np.sin(theta))

        theta += ang_increment
    
    plt.plot(x, y, label= "2D Top View Trajectory (x vs y)")
    plt.legend()
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