import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def import_data(data_idx):
    home_path = os.path.abspath('C:/Users/alexa/Documents/Caltech/Research/Plotting_Code')
    data_path = os.path.abspath('C:/Users/alexa/Documents/Caltech/Research/Data/CRTS_Test_Data/')

    # Changes the directory to where the .dat files are located, creates a list of the data sets in the directory then
    # Returns to the directory where the software is installed.
    os.chdir(data_path)
    data_sets = os.listdir()
    os.chdir(home_path)
    data_set_idx = data_idx
    data_set_path = os.path.join(data_path, data_sets[data_set_idx])

    data = pd.read_csv(data_set_path, usecols=(0, 1, 2), delim_whitespace=True, header=None)
    data = data.sort_values(by=0, ascending=True, ignore_index=True)
    return data

dat = import_data(25)
print(dat)
