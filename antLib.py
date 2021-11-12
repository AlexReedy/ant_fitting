import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


def import_data(filename):
    data_path = os.path.abspath('/home/sedmdev/Research/ant_fitting/CRTS_Test_Data')

    data_set_path = os.path.join(data_path, filename)

    data = pd.read_csv(data_set_path, usecols=(0, 1, 2), delim_whitespace=True, header=None)

    mag_data = data.sort_values(by=0, ascending=True, ignore_index=True)

    flux_data = data.sort_values(by=0, ascending=True, ignore_index=True)
    flux_data[1] = flux_data[1].apply(lambda x: 3631.0 * (10.0 ** (-0.4 * x)))

    return filename, mag_data, flux_data


def make_plot_static(data, fig_title, plot_title, x_title, y_title, mag=False):
    fig, ax = plt.subplots(1)
    fig.set_size_inches(10, 7)
    fig.suptitle(f'{plot_title} [ID: {fig_title[:-4]}]')
    fig.canvas.manager.set_window_title(f'{fig_title[:-4]}_{plot_title}')

    ax.set_xlabel(f'{x_title}')
    ax.set_ylabel(f'{y_title}')

    if not mag:
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        ax.errorbar(data[0],
                    data[1],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    elinewidth=1,
                    color='black')
        plt.show()

    if mag:
        ax.invert_yaxis()
        ax.errorbar(data[0],
                    data[1],
                    yerr=data[2],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    elinewidth=1,
                    color='black')
        plt.show()


def make_plot_dynamic(data, fig_title, plot_title, x_title, y_title, mag=False):
    fig, ax = plt.subplots(1)
    fig.set_size_inches(10, 7)
    fig.suptitle(f'{plot_title} [ID: {fig_title[:-4]}]')
    fig.canvas.manager.set_window_title(f'{fig_title[:-4]}_{plot_title}')

    ax.set_xlabel(f'{x_title}')
    ax.set_ylabel(f'{y_title}')
    ax.set_xlim(xmin=data[0].min() - 100,
                xmax=data[0].max() + 100)

    if not mag:
        for i in range(len(data)):
            ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
            ax.errorbar(data[0][i],
                        data[1][i],
                        linestyle='none',
                        marker='s',
                        ms=3,
                        elinewidth=1,
                        color='black')
            plt.pause(.001)
        plt.show()

    if mag:
        for i in range(len(data)):
            ax.invert_yaxis()
            ax.errorbar(data[0][i],
                        data[1][i],
                        yerr=data[2][i],
                        linestyle='none',
                        marker='s',
                        ms=3,
                        elinewidth=1,
                        color='black')
            plt.pause(.001)
        plt.show()


def make_plot(data, fig_title, plot_title, x_title, y_title, mag=False, dynamic=False):
    if not dynamic:
        make_plot_static(data=data,
                         fig_title=fig_title,
                         plot_title=plot_title,
                         x_title=x_title,
                         y_title=y_title,
                         mag=mag)
    if dynamic:
        make_plot_dynamic(data=data,
                          fig_title=fig_title,
                          plot_title=plot_title,
                          x_title=x_title,
                          y_title=y_title,
                          mag=mag)


