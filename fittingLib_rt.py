import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import getpass

plot_base_color = 'black'
poly_trend_color = 'red'
sigma_trend = 'black'
plt_outline_color = 'orange'


class FittingLibrary():
    def __init__(self, pause=0.5):

        path = f'/home/{getpass.getuser()}/ANT_Fitting'
        if not os.path.exists(path):
            os.mkdir(path)

        self.data_sets = os.listdir(os.path.abspath('/home/sedmdev/Research/ant_fitting/CRTS_Test_Data'))

        self.filename = None
        self.plot_title = None
        self.home_dir = os.path.abspath(path)
        self.current_dir = None

        self.mag_data = None
        self.flux_data = None

        self.poly_order = None
        self.sigma = None

        self.polytrend = None
        self.polytrend_std = None
        self.sigma_idx = None
        self.sigma_clip_data = None

        self.sigma_clip_avg_data = None

        self.pause_time = pause

        self.filehandler = None

    def import_data(self, file):
        self.filename = file
        self.plot_title = f'{self.filename[:-4]}'

        dir_path = f'{self.home_dir}/{self.filename[:-4]}'

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            self.current_dir = os.path.abspath(dir_path)
            os.mkdir(f'{self.current_dir}/Plots')
            os.mkdir(f'{self.current_dir}/Data')

        self.current_dir = os.path.abspath(dir_path)
        self.filehandler = open(f'{self.current_dir}/{self.plot_title}_log.txt', 'w')

        data_path = os.path.abspath('/home/sedmdev/Research/ant_fitting/CRTS_Test_Data')
        data_set_path = os.path.join(data_path, file)
        data = pd.read_csv(data_set_path, usecols=(0, 1, 2), delim_whitespace=True, header=None)
        mag_data = data.sort_values(by=0, ascending=True, ignore_index=True)

        flux_data = data.sort_values(by=0, ascending=True, ignore_index=True)
        flux_data[1] = flux_data[1].apply(lambda x: 3631.0 * (10.0 ** (-0.4 * x)))
        flux_data[2] = .000005

        self.mag_data = mag_data
        self.flux_data = flux_data

        self.mag_data.to_csv(f'{self.current_dir}/Data/{self.plot_title}_sorted_mag.dat',
                             index=False,
                             header=False,
                             )
        self.flux_data.to_csv(f'{self.current_dir}/Data/{self.plot_title}_sorted_flux.dat',
                              index=False,
                              header=False,
                              )

        self.filehandler.close()

    def plot_mag(self, show=True, save=True):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        fig.suptitle(f'{self.plot_title} Magnitude Light Curve')
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

    def plot_mag_dynamic(self, save=True):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        fig.suptitle(f'{self.plot_title} Magnitude Light Curve')
        window_name = f'{self.plot_title}_magnitude_light_curve'
        fig.canvas.manager.set_window_title(window_name)

        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.tick_params(axis='x', colors=plt_outline_color)
        ax.tick_params(axis='y', colors=plt_outline_color)
        ax.yaxis.label.set_color(plt_outline_color)
        ax.xaxis.label.set_color(plt_outline_color)
        ax.spines['bottom'].set_color(plt_outline_color)
        ax.spines['top'].set_color(plt_outline_color)
        ax.spines['left'].set_color(plt_outline_color)
        ax.spines['right'].set_color(plt_outline_color)

        ax.set(xlabel='Modified Julian Day [MJD]', ylabel='Magnitude')
        ax.invert_yaxis()

        for i in range(len(self.mag_data)):
            ax.errorbar(self.mag_data[0][i],
                        self.mag_data[1][i],
                        yerr=self.mag_data[2][i],
                        linestyle='none',
                        marker='s',
                        ms=3,
                        color=plt_outline_color
                        )
            plt.pause(.001)
        plt.pause(self.pause_time)
        plt.show(block=False)
        plt.close()
        if save:
            self.plot_mag(show=False, save=True)

    def plot_flux(self, show=True, save=True):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        fig.suptitle(f'{self.plot_title} Flux Light Curve')
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

    def plot_flux_dynamic(self, save=True):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        fig.suptitle(f'{self.plot_title} Flux Light Curve')
        window_name = f'{self.plot_title}_flux_light_curve'
        fig.canvas.manager.set_window_title(window_name)

        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.tick_params(axis='x', colors=plt_outline_color)
        ax.tick_params(axis='y', colors=plt_outline_color)
        ax.yaxis.label.set_color(plt_outline_color)
        ax.xaxis.label.set_color(plt_outline_color)
        ax.spines['bottom'].set_color(plt_outline_color)
        ax.spines['top'].set_color(plt_outline_color)
        ax.spines['left'].set_color(plt_outline_color)
        ax.spines['right'].set_color(plt_outline_color)

        ax.set(xlabel='Modified Julian Day [MJD]', ylabel='Flux [Jy]')
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        for i in range(len(self.flux_data)):
            ax.errorbar(self.flux_data[0][i],
                        self.flux_data[1][i],
                        yerr=self.flux_data[2][i],
                        linestyle='none',
                        marker='s',
                        ms=3,
                        color=plt_outline_color
                        )
            plt.pause(.001)
        plt.pause(self.pause_time)
        plt.show(block=False)
        plt.close()
        if save:
            self.plot_flux(show=False, save=True)

    def sigma_clipping(self, poly_order=5, sigma=5):
        self.poly_order = poly_order
        self.sigma = sigma

        trend = np.polyfit(self.flux_data[0], self.flux_data[1], self.poly_order)
        self.polytrend = np.polyval(trend, self.flux_data[0])
        self.polytrend_std = self.sigma * np.std(self.polytrend)

        self.sigma_idx = []
        for i in range(len(self.flux_data)):
            if (self.flux_data[1][i] - self.flux_data[2][i]) >= self.polytrend[i] + self.polytrend_std:
                self.sigma_idx.append(i)
            if (self.flux_data[1][i] + self.flux_data[2][i]) <= self.polytrend[i] - self.polytrend_std:
                self.sigma_idx.append(i)

        self.sigma_clip_data = self.flux_data.drop(labels=self.sigma_idx, axis=0, inplace=False).reset_index(drop=True)

        self.sigma_clip_data.to_csv(f'{self.current_dir}/Data/{self.plot_title}_sigma_clipped.dat',
                                    index=False,
                                    header=False,
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
            ax.set_title(f'{self.plot_title} Fifth Order Polynomial Fit')
            window_name = f'{self.plot_title}_polytrend'
            fig.canvas.manager.set_window_title(window_name)
            plt.pause(self.pause_time)
            plt.show(block=False)
        if save:
            plt.savefig(f'{self.current_dir}/Plots/{self.plot_title}_polytrend.png')

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

        if show:
            ax.set_title(f'{self.plot_title} {self.sigma} Sigma Clipping')
            window_name = f'{self.plot_title}_sigma_clipping'
            fig.canvas.manager.set_window_title(window_name)
            plt.pause(self.pause_time)
            plt.show(block=False)
        if save:
            plt.savefig(f'{self.current_dir}/Plots/{self.plot_title}_{self.sigma}sigma_clipping.png')

        ax.errorbar(clipped_x,
                    clipped_y,
                    yerr=clipped_err,
                    linestyle='none',
                    marker='x',
                    ms=4,
                    color='red'
                    )

        if show:
            ax.set_title(f'{self.plot_title} {self.sigma} Sigma Clipping [Excluded Values]')
            window_name = f'{self.plot_title}_{self.sigma}sigma_clipping_show_clipped'
            fig.canvas.manager.set_window_title(window_name)
            plt.pause(self.pause_time)
            plt.show(block=False)
        if save:
            plt.savefig(f'{self.current_dir}/Plots/{self.plot_title}_sigma_clipping_show_clipped.png')

        plt.close()

    def plot_sigma_clip_dynamic(self, save=True):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)

        clipped_x = self.flux_data[0][self.sigma_idx]
        clipped_y = self.flux_data[1][self.sigma_idx]
        clipped_err = self.flux_data[2][self.sigma_idx]

        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.tick_params(axis='x', colors=plt_outline_color)
        ax.tick_params(axis='y', colors=plt_outline_color)
        ax.yaxis.label.set_color(plt_outline_color)
        ax.xaxis.label.set_color(plt_outline_color)
        ax.spines['bottom'].set_color(plt_outline_color)
        ax.spines['top'].set_color(plt_outline_color)
        ax.spines['left'].set_color(plt_outline_color)
        ax.spines['right'].set_color(plt_outline_color)

        ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        ax.set(xlabel='Modified Julian Day [MJD]', ylabel='Flux [Jy]')
        ax.errorbar(self.flux_data[0],
                    self.flux_data[1],
                    yerr=self.flux_data[2],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    color=plt_outline_color
                    )

        ax.plot(self.flux_data[0],
                self.polytrend,
                linestyle='--',
                linewidth='1',
                color=plt_outline_color)

        ax.plot(self.flux_data[0],
                self.polytrend - self.polytrend_std,
                linestyle='--',
                linewidth='1',
                color=plt_outline_color)

        ax.plot(self.flux_data[0],
                self.polytrend + self.polytrend_std,
                linestyle='--',
                linewidth='1',
                color=plt_outline_color)

        plt.pause(self.pause_time)

        ax.errorbar(self.sigma_clip_data[0],
                    self.sigma_clip_data[1],
                    yerr=self.sigma_clip_data[2],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    color='lime'
                    )

        plt.pause(self.pause_time)

        ax.errorbar(clipped_x,
                    clipped_y,
                    yerr=clipped_err,
                    linestyle='none',
                    marker='x',
                    ms=4,
                    color='red'
                    )

        plt.pause(self.pause_time)
        plt.show(block=False)
        plt.close()

        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        ax.set(xlabel='Modified Julian Day [MJD]', ylabel='Flux [Jy]')

        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.tick_params(axis='x', colors=plt_outline_color)
        ax.tick_params(axis='y', colors=plt_outline_color)
        ax.yaxis.label.set_color(plt_outline_color)
        ax.xaxis.label.set_color(plt_outline_color)
        ax.spines['bottom'].set_color(plt_outline_color)
        ax.spines['top'].set_color(plt_outline_color)
        ax.spines['left'].set_color(plt_outline_color)
        ax.spines['right'].set_color(plt_outline_color)

        ax.errorbar(self.sigma_clip_data[0],
                    self.sigma_clip_data[1],
                    yerr=self.sigma_clip_data[2],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    color=plt_outline_color
                    )

        ax.plot(self.flux_data[0],
                self.polytrend,
                linestyle='--',
                linewidth='1',
                color=plt_outline_color)

        ax.plot(self.flux_data[0],
                self.polytrend - self.polytrend_std,
                linestyle='--',
                linewidth='1',
                color=plt_outline_color)

        ax.plot(self.flux_data[0],
                self.polytrend + self.polytrend_std,
                linestyle='--',
                linewidth='1',
                color=plt_outline_color)

        plt.pause(self.pause_time)
        plt.show(block=False)
        plt.close()

        if save:
            self.plot_sigma_clip(show=False, save=True)


    def get_average(self):
        unique_days_str = np.unique(self.sigma_clip_data[0].apply(lambda x: str(x)[0:5]))
        unique_days = []
        unique_fluxes_avg = []
        unique_errors_avg = []

        for i in range(len(unique_days_str)):
            flux_list_per_obs = []
            unique_days.append(int(unique_days_str[i]))
            unique_errors_avg.append(.0005)
            for j in range(len(self.sigma_clip_data)):
                if unique_days_str[i] == str(self.sigma_clip_data[0][j])[0:5]:
                    flux_list_per_obs.append(self.sigma_clip_data[1][j])
            unique_fluxes_avg.append(np.average(flux_list_per_obs))

        self.sigma_clip_avg_data = pd.DataFrame([unique_days, unique_fluxes_avg, unique_errors_avg]).T
        self.sigma_clip_avg_data.to_csv(f'{self.current_dir}/Data/{self.plot_title}_sigma_clip_avg_data.dat',
                                        index=False,
                                        header=False,
                                        )

    def plot_sigma_clip_avg(self, show=True, save=True):
        fig, ax = plt.subplots(1)
        fig.set_size_inches(10, 7)
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        ax.set(xlabel='Modified Julian Day [MJD]', ylabel='Flux [Jy]')
        ax.errorbar(self.sigma_clip_avg_data[0],
                    self.sigma_clip_avg_data[1],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    color='black'
                    )
        plt.show()
