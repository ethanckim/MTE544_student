import matplotlib.pyplot as plt
from utilities import FileReader

def plot_xy(filename):
    headers, values=FileReader(filename).read_file() 
    x_data=[lin[0] for lin in values]
    y_data=[lin[1] for lin in values]
    
    plt.plot(x_data, y_data, label= "2D Top View Trajectory (x vs y)")
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
        plot_xy(filename)