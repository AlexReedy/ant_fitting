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
    def __init__(self, pause=0.5,
                 user='default',
                 poly_degree=5,
                 sigma_coefficient=5,
                 offset_prct=20,
                 flux_error=.000005):

        # Checks to see if a directory for all fitting files exists, if not then it makes one in the users home folder
        path = f'/home/{getpass.getuser()}/ANT_Fitting'
        if not os.path.exists(path):
            os.mkdir(path)

        self.pause_time = pause
        self.log_file = None
        self.user = user
        self.flux_error = flux_error

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
        self.sigma_excluded = None
        self.sigma_retained = None

        self.sigma_clip_data = None
        self.sigma_clip_data_length = None
        self.sigma_clip_data_peak_idx = None
        self.sigma_clip_data_peak_list = None
        self.sigma_clip_data_time_range_list = None

        # Variables for the Sigma Clipped and Averaged Data Frame
        self.avg_data = None
        self.avg_data_length = None
        self.avg_data_peak_idx = None
        self.avg_data_peak_list = None
        self.avg_data_time_range_list = None

        # Variables For Determining Fit Parameters (NOTE: THESE ALL DEPEND ON THE AVERAGED DATA SET!)
        # General:
        self.offset_prct = (offset_prct / 100)
        self.num_offset_detections = None

        # Gaussian:
        self.gaussian_data = None
        self.r_g = None
        self.a_g = None
        self.t_g = None

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
        flux_data[2] = self.flux_error  # This is a placeholder

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
                            f'Source Path: {data_set_path}\n'
                            f'Date: {get_datetime()[0]} @ {get_datetime()[1]}\n'
                            f'User: {self.user}\n'
                            f'\n'
                            )

        self.log_file.write(f'RAW DATA INFORMATION\n'
                            f' > Total Detections: {self.raw_data_length}\n'
                            f' > Peak Index: {self.raw_data_peak_idx}\n'
                            f' > Peak Time (tp,raw): {self.raw_data_peak_list[0]} MJD\n'
                            f' > Peak Amplitude (Ap,raw): {self.raw_data_peak_list[1]} Mag\n'
                            f'\n'
                            )

        self.log_file.write(f'MAGNITUDE DATA INFORMATION\n'
                            f' > Total Detections: {self.mag_data_length}\n'
                            f' > Peak Index: {self.mag_data_peak_idx}\n'
                            f' > Peak Time (tp,mag): {self.mag_data_peak_list[0]} MJD\n'
                            f' > Peak Amplitude (Ap,mag): {self.mag_data_peak_list[1]} Mag\n'
                            f'\n'
                            )

        self.log_file.write(f'FlUX DATA INFORMATION\n'
                            f' > Total Detections: {self.flux_data_length}\n'
                            f' > Peak Index: {self.flux_data_peak_idx}\n'
                            f' > Peak Time (tp,flux): {self.flux_data_peak_list[0]} MJD\n'
                            f' > Peak Amplitude (Ap,flux): {self.flux_data_peak_list[1]} Jy\n'
                            f'\n'
                            )

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
        self.sigma_clip_data_length = len(self.sigma_clip_data)
        self.sigma_clip_data_peak_idx = self.sigma_clip_data[1].idxmax()
        self.sigma_clip_data_peak_list = [self.sigma_clip_data[0][self.sigma_clip_data_peak_idx],
                                          self.sigma_clip_data[1][self.sigma_clip_data_peak_idx]]

        self.sigma_clip_data.to_csv(f'{self.current_dir}/Data/{self.plot_title}_sigma_clipped.dat',
                                    index=False,
                                    header=False,
                                    )

        self.sigma_excluded = [len(self.sigma_idx), ((len(self.sigma_idx) / self.flux_data_length) * 100.0)]
        self.sigma_retained = [len(self.sigma_clip_data), ((len(self.sigma_clip_data) / self.flux_data_length) * 100.0)]

        self.log_file.write(f'POLYNOMIAL FITTING INFORMATION\n'
                            f' > Polynomial Format: (ax^5) + (bx^4) + (cx^3) + (dx^2) + (ex) + (f)\n'
                            f' > Degree: {self.poly_degree}\n'
                            f' > Calculated Sigma: {self.polytrend_sigma}\n'
                            f' > Coefficients (From Highest to Lowest Power):\n'
                            f'    a = {poly_coefficients[0]}\n'
                            f'    b = {poly_coefficients[1]}\n'
                            f'    c = {poly_coefficients[2]}\n'
                            f'    d = {poly_coefficients[3]}\n'
                            f'    e = {poly_coefficients[4]}\n'
                            f'    f = {poly_coefficients[5]}\n'
                            f'\n'
                            )

        self.log_file.write(f'SIGMA CLIPPING INFORMATION\n'
                            f' > Clipping Bound: (+/-) {self.sigma_coefficient} Sigma\n'
                            f' > Excluded {self.sigma_excluded[0]} of {self.flux_data_length} Detections ({self.sigma_excluded[1]} %)\n'
                            f' > Retained {self.sigma_retained[0]} of {self.flux_data_length} Detections ({self.sigma_retained[1]} %)\n'
                            f'\n'
                            )

        self.log_file.write(f'SIGMA CLIPPED DATA INFORMATION\n'
                            f' > Total Detections: {self.sigma_clip_data_length}\n'
                            f' > Peak Index: {self.sigma_clip_data_peak_idx}\n'
                            f' > Peak Time (tp,sig): {self.sigma_clip_data_peak_list[0]} MJD\n'
                            f' > Peak Amplitude (Ap,sig): {self.sigma_clip_data_peak_list[1]} Jy\n'
                            f'\n'
                            )


    def plot_sigma_clip(self, show=True, save=True):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)

        clipped_x = self.flux_data[0][self.sigma_idx]
        clipped_y = self.flux_data[1][self.sigma_idx]
        clipped_err = self.flux_data[2][self.sigma_idx]

        ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        ax.set(xlabel='Modified Julian Day [MJD]', ylabel='Flux [Jy]')
        ax.errorbar(self.sigma_clip_data[0],
                    self.sigma_clip_data[1],
                    yerr=self.sigma_clip_data[2],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    color='black'
                    )

        ax.plot(self.flux_data[0],
                self.polytrend,
                linestyle='--',
                linewidth='1',
                color='black')

        if show:
            ax.set_title(f'{self.plot_title} Polynomial Fit')
            window_name = f'{self.plot_title}_polytrend'
            fig.canvas.manager.set_window_title(window_name)
            plt.pause(self.pause_time)
            plt.show(block=False)
        if save:
            plt.savefig(f'{self.current_dir}/Plots/{self.plot_title}_polytrend.png')

        ax.plot(self.flux_data[0],
                self.polytrend - self.polytrend_sigma,
                linestyle='--',
                linewidth='1',
                color='black')

        ax.plot(self.flux_data[0],
                self.polytrend + self.polytrend_sigma,
                linestyle='--',
                linewidth='1',
                color='black')

        ax.fill_between(self.flux_data[0],
                        self.polytrend - self.polytrend_sigma,
                        self.polytrend + self.polytrend_sigma,
                        color='whitesmoke')

        if show:
            ax.set_title(f'{self.plot_title} Sigma Clipping')
            window_name = f'{self.plot_title}_sigma_clipping'
            fig.canvas.manager.set_window_title(window_name)
            plt.pause(self.pause_time)
            plt.show(block=False)
        if save:
            plt.savefig(f'{self.current_dir}/Plots/{self.plot_title}_sigma_clipping.png')

        ax.errorbar(clipped_x,
                    clipped_y,
                    yerr=clipped_err,
                    linestyle='none',
                    marker='x',
                    ms=4,
                    color='red'
                    )

        if show:
            ax.set_title(f'{self.plot_title} Sigma Clipping [Show Excluded]')
            window_name = f'{self.plot_title}_sigma_clipping_show_clipped'
            fig.canvas.manager.set_window_title(window_name)
            plt.pause(self.pause_time)
            plt.show(block=False)
        if save:
            plt.savefig(f'{self.current_dir}/Plots/{self.plot_title}_sigma_clipping_show_clipped.png')

        plt.close()

    def get_average(self):
        unique_days_str = np.unique(self.sigma_clip_data[0].apply(lambda x: str(x)[0:5]))
        unique_days = []
        unique_fluxes_avg = []
        unique_errors_avg = []

        for i in range(len(unique_days_str)):
            flux_list_per_obs = []
            unique_days.append(int(unique_days_str[i]))
            unique_errors_avg.append(self.flux_error)
            for j in range(len(self.sigma_clip_data)):
                if unique_days_str[i] == str(self.sigma_clip_data[0][j])[0:5]:
                    flux_list_per_obs.append(self.sigma_clip_data[1][j])
            unique_fluxes_avg.append(np.average(flux_list_per_obs))

        self.avg_data = pd.DataFrame([unique_days, unique_fluxes_avg, unique_errors_avg]).T
        self.avg_data_length = len(self.avg_data)
        self.avg_data_peak_idx = self.avg_data[1].idxmax()
        self.avg_data_peak_list = [self.avg_data[0][self.avg_data_peak_idx],
                                   self.avg_data[1][self.avg_data_peak_idx]]

        self.avg_data.to_csv(f'{self.current_dir}/Data/{self.plot_title}_sigma_clip_avg_data.dat', index=False, header=False)

        self.log_file.write(f'AVERAGED DATA INFORMATION\n'
                            f' > Total Detections: {self.avg_data_length}\n'
                            f' > Peak Index: {self.avg_data_peak_idx}\n'
                            f' > Peak Time (tp): {self.avg_data_peak_list[0]} MJD\n'
                            f' > Peak Amplitude (Ap): {self.avg_data_peak_list[1]} Jy\n'
                            f'\n'
                            )

    def plot_avg(self, show=True, save=True):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        ax.set_title(f'{self.plot_title} Light Curve [Averaged]')
        window_name = f'{self.plot_title}_avg_light_curve'
        fig.canvas.manager.set_window_title(window_name)

        ax.set(xlabel='Modified Julian Day [MJD]', ylabel='Flux [Jy]')
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        ax.errorbar(self.avg_data[0],
                    self.avg_data[1],
                    yerr=self.avg_data[2],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    color='black'
                    )

        # Plots the Peak Location:
        ax.errorbar(self.avg_data[0][self.avg_data_peak_idx],
                    self.avg_data[1][self.avg_data_peak_idx],
                    yerr=self.avg_data[2][self.avg_data_peak_idx],
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

    def get_fit_parameters(self):
        self.num_offset_detections = int(np.round(self.avg_data_length * self.offset_prct))

        # Gaussian Parameters:
        self.gaussian_data = self.avg_data[0:self.avg_data_peak_idx+1]
        self.r_g = np.mean(self.gaussian_data[1][0:self.num_offset_detections])
        self.a_g = self.gaussian_data[1] - self.r_g
        self.t_g = np.var(self.gaussian_data[0][0:self.avg_data_peak_idx])

        self.log_file.write(f'GAUSSIAN FITTING PARAMETERS\n'
                            f' > Number of Detections:')

    def plot_fitting_parameters(self, show=True, save=True):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        ax.set_title(f'{self.plot_title} Light Curve [Fit Parameters]')
        window_name = f'{self.plot_title}_avg_fit_light_curve'
        fig.canvas.manager.set_window_title(window_name)

        ax.set(xlabel='Modified Julian Day [MJD]', ylabel='Flux [Jy]')
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))

        # Plots The Averaged Data Set
        ax.errorbar(self.avg_data[0],
                    self.avg_data[1],
                    yerr=self.avg_data[2],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    color='black'
                    )

        # Plots the Horizontal and Vertical Lines for the Peak


        if save:
            plt.savefig(f'{self.current_dir}/Plots/{window_name}.png')

        if show:
            plt.pause(self.pause_time)
            plt.show(block=False)
            plt.close()

        plt.close()





