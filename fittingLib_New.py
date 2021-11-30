import time
import timeit
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import getpass

plot_base_color = 'black'
poly_trend_color = 'red'
sigma_trend = 'black'


def get_datetime():
    time_stamp = f'{time.strftime("%I")}:{time.strftime("%M")}:{time.strftime("%S")}{time.strftime("%p")}'
    date_time = f'[{time_stamp}]'
    return date_time


class FittingLibrary():
    def __init__(self, pause=0.5, user='ahreedy', poly_order=5, sigma_coefficient=5, offset_prct=0.02):

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

        self.total_detections = None
        self.mag_data = None
        self.flux_data = None

        self.poly_order = poly_order
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

        self.r_g = None
        self.a_g = None
        self.t_g = None
        self.t_rise = None
        self.gaussian = None

        self.exponential_baseline_data = None
        self.r_e = None
        self.a_e = None

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
        start_date = data[0][data[0].idxmin()]
        end_date = data[0][data[0].idxmax()]


        # Creates a new dataframe for the sorted magnitude data
        mag_data = data.sort_values(by=0, ascending=True, ignore_index=True)

        # Creates a new dataframe for the sorted data that has been converted from magnitude to flux
        # Also sets the error value to be used for the flux data
        flux_data = data.sort_values(by=0, ascending=True, ignore_index=True)
        flux_data[1] = flux_data[1].apply(lambda x: 3631.0 * (10.0 ** (-0.4 * x)))
        flux_data[2] = .000005  # This is a placeholder

        self.mag_data = mag_data
        self.flux_data = flux_data

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
        self.log_file.write(f'SOURCE ID: {file}\n')
        self.log_file.write(f'SOURCE PATH: {data_set_path}\n')
        self.log_file.write(f'USER: {self.user}\n\n')

        self.log_file.write(f'TOTAL DETECTIONS: {len(self.flux_data)}\n')
        self.log_file.write(f'DATE OF FIRST DETECTION (MJD): {start_date}\n')
        self.log_file.write(f'DATE OF LAST DETECTION (MJD): {end_date}\n')
        self.log_file.write(f'TOTAL TIME (MJD): {end_date - start_date}\n\n')


    def plot_mag(self, show=True, save=True):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        ax.set_title(f'{self.plot_title} Light Curve [Magnitude]')
        window_name = f'{self.plot_title}_magnitude_light_curve'
        fig.canvas.manager.set_window_title(window_name)

        ax.set(xlabel='Modified Julian Day [MJD]', ylabel='Magnitude')
        ax.invert_yaxis()
        ax.errorbar(self.mag_data[0],
                    self.mag_data[1],
                    yerr=self.mag_data[2],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    color='black'
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

        if save:
            plt.savefig(f'{self.current_dir}/Plots/{window_name}.png')

        if show:
            plt.pause(self.pause_time)
            plt.show(block=False)
            plt.close()

        plt.close()

    def sigma_clipping(self):
        # Returns the coefiicients of the polynomial fit
        poly_coefficients = np.polyfit(self.flux_data[0], self.flux_data[1], self.poly_order)
        poly_coefficients_varlist = ['a', 'b', 'c', 'd', 'e']

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
        self.sigma_excluded = [len(self.sigma_idx), int((len(self.sigma_idx) / len(self.flux_data)) * 100.0)]
        self.sigma_retained = [len(self.sigma_clip_data), int((len(self.sigma_clip_data) / len(self.flux_data)) * 100.0)]

        self.log_file.write(f'POLYNOMIAL ORDER: {self.poly_order} \n')
        self.log_file.write(f'POLYNOMIAL COEFFICIENTS: \n')
        for i in range(self.poly_order):
            self.log_file.write(f' {poly_coefficients_varlist[i]}: {poly_coefficients[i]}\n')

        self.log_file.write(f'\nSIGMA CLIPPING PERFORMED AT: +/- {self.sigma_coefficient} Sigma\n')
        self.log_file.write(f' CLIPPING EXCLUDED {self.sigma_excluded[0]} of :'
                            f' {self.sigma_excluded[1]} % ')


        self.log_file.write(f' > CLIPPING RETAINED:'
                            f' {int((len(self.sigma_clip_data) / len(self.flux_data)) * 100.0)} %'
                            f' [{len(self.sigma_clip_data)} of {len(self.flux_data)}]\n\n')

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