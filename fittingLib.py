import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import getpass

plot_base_color = 'black'
poly_trend_color = 'red'
sigma_trend = 'black'


class FittingLibrary():
    def __init__(self):
        path = f'/home/{getpass.getuser()}/ANT_Fitting'
        if not os.path.exists(path):
            os.mkdir(path)

        self.filename = None
        self.plot_title = None
        self.home_dir = os.path.abspath(path)
        self.current_dir = None

        self.mag_data = None
        self.flux_data = None

        self.polytrend = None
        self.polytrend_std = None
        self.sigma_idx = None
        self.sigma_clip_data = None

    def import_data(self, file):
        self.filename = file
        self.plot_title = f'{self.filename[:-4]}'

        dir_path = f'{self.home_dir}/{self.filename[:-4]}'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            self.current_dir = os.path.abspath(dir_path)
        self.current_dir = os.path.abspath(dir_path)

        data_path = os.path.abspath('/home/sedmdev/Research/ant_fitting/CRTS_Test_Data')
        data_set_path = os.path.join(data_path, file)
        data = pd.read_csv(data_set_path, usecols=(0, 1, 2), delim_whitespace=True, header=None)
        mag_data = data.sort_values(by=0, ascending=True, ignore_index=True)
        flux_data = data.sort_values(by=0, ascending=True, ignore_index=True)
        flux_data[1] = flux_data[1].apply(lambda x: 3631.0 * (10.0 ** (-0.4 * x)))

        self.mag_data = mag_data
        self.flux_data = flux_data

    def plot_mag(self, save=False):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        fig.suptitle(f'{self.plot_title} Magnitude Light Curve')
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        ax.invert_yaxis()

        ax.errorbar(self.mag_data[0],
                    self.mag_data[1],
                    yerr=self.mag_data[2],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    color='black'
                    )
        plt.pause(2)
        plt.show(block=False)

    def sigma_clipping(self, poly_order, sigma):
        trend = np.polyfit(self.flux_data[0], self.flux_data[1], poly_order)
        self.polytrend = np.polyval(trend, self.flux_data[0])
        self.polytrend_std = sigma * np.std(self.polytrend)

        self.sigma_idx = []
        for i in range(len(self.flux_data)):
            if self.flux_data[1][i] >= self.polytrend[i] + self.polytrend_std:
                self.sigma_idx.append(i)
            if self.flux_data[1][i] <= self.polytrend[i] - self.polytrend_std:
                self.sigma_idx.append(i)

        self.sigma_clip_data = self.flux_data.drop(labels=self.sigma_idx, axis=0, inplace=False).reset_index(drop=True)

    def plot_sigma_clip(self, show_clipped=False, save=False):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        fig.suptitle(f'{self.plot_title} Sigma Clipping')
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))

        clipped_x = self.flux_data[0][self.sigma_idx]
        clipped_y = self.flux_data[1][self.sigma_idx]

        ax.errorbar(self.sigma_clip_data[0],
                    self.sigma_clip_data[1],
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

        ax.plot(self.flux_data[0],
                self.polytrend - self.polytrend_std,
                linestyle='--',
                linewidth='1',
                color='black')

        ax.plot(self.flux_data[0],
                self.polytrend + self.polytrend_std,
                linestyle='--',
                linewidth='1',
                color='black')

        if show_clipped:
            ax.errorbar(clipped_x,
                        clipped_y,
                        linestyle='none',
                        marker='x',
                        ms=4,
                        color='red'
                        )
        plt.pause(2)
        plt.show(block=False)
        if save:
            plt.savefig(f'{self.current_dir}/{self.plot_title}_sigma_clipping.png')
