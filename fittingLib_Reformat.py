import time
import timeit
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import getpass

def get_datetime():
    # DATE STRINGS
    month = time.strftime("%m")
    day = time.strftime("%d")
    year = time.strftime("%Y")

    # TIME STRINGS
    hour = time.strftime("%I")
    min = time.strftime("%M")
    sec = time.strftime("%S")
    am_pm = time.strftime("%p")

    date_stamp = f'{month}.{day}.{year}'
    time_stamp = f'{hour}:{min}:{sec} {am_pm}'
    return date_stamp, time_stamp

class FittingLibrary():
    def __init__(self, pause=0.5, user='default', poly_degree=5, sigma_coefficient=5, offset_prct=0.02):

        # Checks to see if a directory for all fitting files exists, if not then it makes one in the users home folder
        path = f'/home/{getpass.getuser()}/ANT_Fitting'
        if not os.path.exists(path):
            os.mkdir(path)

        self.pause_time = pause
        self.log_file = None
        self.user = user

        self.data_sets = os.listdir(os.path.abspath('/home/sedmdev/Research/ant_fitting/CRTS_Test_Data'))
        self.filename = None
        self.plot_title = None
        self.home_dir = os.path.abspath(path)
        self.current_dir = None

        self.raw_data = None
        self.raw_data_length = None
        self.raw_data_peak_idx = None
        self.raw_data_peak_list = None
        self.raw_data_time_range_list = None

        self.mag_data = None
        self.mag_data_length = None
        self.mag_data_peak_idx = None
        self.mag_data_peak_list = None
        self.mag_data_time_range_list = None

        self.flux_data = None
        self.flux_data_length = None
        self.flux_data_peak_idx = None
        self.flux_data_peak_list = None
        self.flux_data_time_range_list = None

        self.poly_degree = poly_degree
        self.sigma_coefficient = sigma_coefficient
        self.polytrend = None
        self.polytrend_sigma = None
        self.sigma_idx = None
        self.sigma_clip_data = None
        self.sigma_excluded = None
        self.sigma_retained = None

        self.sigma_clip_avg_data = None
        self.post_avg_peak_idx = None
        self.a_p = None
        self.t_p = None

        self.offset_prct = offset_prct

    def import_data(self, file):
        self.filename = file
        self.plot_title = f'{self.filename[:-4]}'

        dir_path = f'{self.home_dir}/{self.filename[:-4]}'
        # Checks to see if a directory for this data set exists, if it doesn't then it creates one
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)  # Makes the data set directory
            self.current_dir = os.path.abspath(dir_path)
            os.mkdir(f'{self.current_dir}/Plots')  # Makes a "Plots" subdirectory
            os.mkdir(f'{self.current_dir}/Data')  # Makes a "Data" subdirectory
        self.current_dir = os.path.abspath(dir_path)

        # Finds the data set based on the filename provided and creates a dataframe
        data_path = os.path.abspath('/home/sedmdev/Research/ant_fitting/CRTS_Test_Data')
        data_set_path = os.path.join(data_path, file)
        data = pd.read_csv(data_set_path, usecols=(0, 1, 2), delim_whitespace=True, header=None)

        # Creates a new dataframe for the sorted magnitude data
        mag_data = data.sort_values(by=0, ascending=True, ignore_index=True)

        # Creates a new dataframe for the sorted data that has been converted from magnitude to flux
        # Also sets the error value to be used for the flux data
        flux_data = data.sort_values(by=0, ascending=True, ignore_index=True)
        flux_data[1] = flux_data[1].apply(lambda x: 3631.0 * (10.0 ** (-0.4 * x)))
        flux_data[2] = .000005  # This is a placeholder

        self.raw_data = data
        self.raw_data_length = len(self.raw_data)
        self.raw_data_peak_idx = self.raw_data[1].idxmin()
        self.raw_data_peak_list = [self.raw_data[0][self.raw_data_peak_idx],
                                   self.raw_data[1][self.raw_data_peak_idx]]

        self.mag_data = mag_data
        self.mag_data_length = len(self.mag_data)
        self.mag_data_peak_idx = self.mag_data[1].idxmin()
        self.mag_data_peak_list = [self.mag_data[0][self.mag_data_peak_idx],
                                   self.mag_data[1][self.mag_data_peak_idx]]

        self.flux_data = flux_data
        self.flux_data_length = len(self.flux_data)
        self.flux_data_peak_idx = self.flux_data[1].idxmax()
        self.flux_data_peak_list = [self.flux_data[0][self.flux_data_peak_idx],
                                    self.flux_data[1][self.flux_data_peak_idx]]

        # Saves two new data frames. One for the sorted magnitude data, and one for the sorted flux data, saves to
        # the "Data" subdirectory
        self.mag_data.to_csv(f'{self.current_dir}/Data/{self.plot_title}_sorted_mag.dat',
                             index=False,
                             header=False,
                             )

        self.flux_data.to_csv(f'{self.current_dir}/Data/{self.plot_title}_sorted_flux.dat',
                              index=False,
                              header=False,
                              )

        # Writes out basic info taken from the import
        self.log_file = open(f'{self.current_dir}/{self.plot_title}_log.txt', 'w')
        self.log_file.write(f'RUN INFORMATION\n'
                            f'Source ID: {file}\n'
                            f'Source Path: {data_set_path}\n\n'
                            f'Date: {get_datetime()[0]} @ {get_datetime()[1]}\n'
                            f'User: {self.user}\n\n')

        self.log_file.write(f'RAW DATA INFORMATION\n'
                            f' > Total Detections: {self.raw_data_length}\n'
                            f' > Peak Index: {self.raw_data_peak_idx}\n'
                            f' > Peak Time (tp,raw): {self.raw_data_peak_list[0]} [MJD]\n'
                            f' > Peak Amplitude (Ap,raw): {self.raw_data_peak_list[1]} [Mag]\n\n')

        self.log_file.write(f'MAGNITUDE DATA INFORMATION\n'
                            f' > Total Detections: {self.mag_data_length}\n'
                            f' > Peak Index: {self.mag_data_peak_idx}\n'
                            f' > Peak Time (tp,mag): {self.mag_data_peak_list[0]} [MJD]\n'
                            f' > Peak Amplitude (Ap,mag): {self.mag_data_peak_list[1]} [Mag]\n\n')

        self.log_file.write(f'FlUX DATA INFORMATION\n'
                            f' > Total Detections: {self.flux_data_length}\n'
                            f' > Peak Index: {self.flux_data_peak_idx}\n'
                            f' > Peak Time (tp,flux): {self.flux_data_peak_list[0]} [MJD]\n'
                            f' > Peak Amplitude (Ap,flux): {self.flux_data_peak_list[1]} [Jy]\n\n')

    def plot_raw(self, show=True, save=True):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        ax.set_title(f'{self.plot_title} Light Curve [Raw]')
        window_name = f'{self.plot_title}_raw_magnitude_light_curve'
        fig.canvas.manager.set_window_title(window_name)

        ax.set(xlabel='Modified Julian Day [MJD]', ylabel='Magnitude')
        ax.invert_yaxis()

        # Plots the Light Curve:
        ax.errorbar(self.raw_data[0],
                    self.raw_data[1],
                    yerr=self.raw_data[2],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    color='black'
                    )

        # Plots the Peak Location:
        ax.errorbar(self.raw_data[0][self.raw_data_peak_idx],
                    self.raw_data[1][self.raw_data_peak_idx],
                    yerr=self.raw_data[2][self.raw_data_peak_idx],
                    linestyle='none',
                    marker='s',
                    ms=5,
                    color='red'
                    )

        if save:
            plt.savefig(f'{self.current_dir}/Plots/{window_name}.png')

        if show:
            plt.pause(self.pause_time)
            plt.show(block=False)
            plt.close()

        plt.close()

    def plot_mag(self, show=True, save=True):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        ax.set_title(f'{self.plot_title} Light Curve [Magnitude]')
        window_name = f'{self.plot_title}_magnitude_light_curve'
        fig.canvas.manager.set_window_title(window_name)

        ax.set(xlabel='Modified Julian Day [MJD]', ylabel='Magnitude')
        ax.invert_yaxis()
        # Plots the Light Curve
        ax.errorbar(self.mag_data[0],
                    self.mag_data[1],
                    yerr=self.mag_data[2],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    color='black'
                    )

        # Plots the Peak Location:
        ax.errorbar(self.mag_data[0][self.mag_data_peak_idx],
                    self.mag_data[1][self.mag_data_peak_idx],
                    yerr=self.mag_data[2][self.mag_data_peak_idx],
                    linestyle='none',
                    marker='s',
                    ms=5,
                    color='red'
                    )

        if save:
            plt.savefig(f'{self.current_dir}/Plots/{window_name}.png')

        if show:
            plt.pause(self.pause_time)
            plt.show(block=False)
            plt.close()

        plt.close()

    def plot_flux(self, show=True, save=True):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        ax.set_title(f'{self.plot_title} Light Curve [Flux]')
        window_name = f'{self.plot_title}_flux_light_curve'
        fig.canvas.manager.set_window_title(window_name)

        ax.set(xlabel='Modified Julian Day [MJD]', ylabel='Flux [Jy]')
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        ax.errorbar(self.flux_data[0],
                    self.flux_data[1],
                    yerr=self.flux_data[2],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    color='black'
                    )

        # Plots the Peak Location:
        ax.errorbar(self.flux_data[0][self.flux_data_peak_idx],
                    self.flux_data[1][self.flux_data_peak_idx],
                    yerr=self.flux_data[2][self.flux_data_peak_idx],
                    linestyle='none',
                    marker='s',
                    ms=5,
                    color='red'
                    )

        if save:
            plt.savefig(f'{self.current_dir}/Plots/{window_name}.png')

        if show:
            plt.pause(self.pause_time)
            plt.show(block=False)
            plt.close()

        plt.close()

    def sigma_clipping(self):
        # Returns the coefiicients of the polynomial fit
        poly_coefficients = np.polyfit(self.flux_data[0], self.flux_data[1], self.poly_degree)

        self.polytrend = np.polyval(poly_coefficients, self.flux_data[0])
        self.polytrend_sigma = self.sigma_coefficient * np.std(self.polytrend)

        self.sigma_idx = []
        for i in range(len(self.flux_data)):
            if (self.flux_data[1][i] - self.flux_data[2][i]) >= self.polytrend[i] + self.polytrend_sigma:
                self.sigma_idx.append(i)
            if (self.flux_data[1][i] + self.flux_data[2][i]) <= self.polytrend[i] - self.polytrend_sigma:
                self.sigma_idx.append(i)

        self.sigma_clip_data = self.flux_data.drop(labels=self.sigma_idx, axis=0, inplace=False).reset_index(drop=True)

        self.sigma_clip_data.to_csv(f'{self.current_dir}/Data/{self.plot_title}_sigma_clipped.dat',
                                    index=False,
                                    header=False,
                                    )

        self.sigma_excluded = [len(self.sigma_idx), ((len(self.sigma_idx) / self.total_detections) * 100.0)]
        self.sigma_retained = [len(self.sigma_clip_data), ((len(self.sigma_clip_data) / self.total_detections) * 100.0)]
