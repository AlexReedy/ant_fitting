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


def make_plot(data, fig_title, plot_title, x_title, y_title, mag=False, dynamic=False):
    fig, ax = plt.subplots(1)
    fig.set_size_inches(10, 7)
    fig.suptitle(f'{plot_title} [ID: {fig_title[:-4]}]')
    fig.canvas.manager.set_window_title(f'{fig_title[:-4]}_{plot_title}')

    ax.set_xlabel(f'{x_title}')
    ax.set_ylabel(f'{y_title}')

    if not dynamic:
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
    if dynamic:
        if not mag:
            ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
            for i in range(len(data)):
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


def plot_mag_flux(data1, data2, fig_title, dynamic=False):
    fig, ax = plt.subplots(2)
    fig.set_size_inches(10, 8)
    fig.canvas.manager.set_window_title(f'{fig_title[:-4]}_Mag_Flux_Comparison')
    fig.suptitle(f'CRTS {fig_title[:-4]}')

    ax[0].set_title('Magnitude')
    ax[0].set_xlabel('Modified Julian Day')
    ax[0].set_ylabel('Magnitude')
    ax[0].invert_yaxis()

    ax[1].set_title(f'Flux')
    ax[1].set_xlabel('Modified Julian Day')
    ax[1].set_ylabel('Flux')
    ax[1].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))

    if not dynamic:
        ax[0].errorbar(data1[0],
                       data1[1],
                       yerr=data1[2],
                       linestyle='none',
                       marker='s',
                       ms=3,
                       elinewidth=1,
                       color='black')

        ax[1].errorbar(data2[0],
                       data2[1],
                       linestyle='none',
                       marker='s',
                       ms=3,
                       elinewidth=1,
                       color='black')

        fig.tight_layout()
        plt.show()

    if dynamic:
        ax[0].set_xlim(xmin=data1[0].min() - 100,
                       xmax=data1[0].max() + 100)

        ax[1].set_xlim(xmin=data2[0].min() - 100,
                       xmax=data2[0].max() + 100)

        for i in range(len(data1)):
            ax[0].errorbar(data1[0][i],
                           data1[1][i],
                           yerr=data1[2][i],
                           linestyle='none',
                           marker='s',
                           ms=3,
                           elinewidth=1,
                           color='black')

            ax[1].errorbar(data2[0][i],
                           data2[1][i],
                           linestyle='none',
                           marker='s',
                           ms=3,
                           elinewidth=1,
                           color='black')

            plt.pause(.001)
            fig.tight_layout()
        plt.show()


def sigma_clipping(data, poly_order, sigma, fill=False):
    trend = np.polyfit(data[0], data[1], poly_order)
    polytrend = np.polyval(trend, data[0])
    polytrend_std = sigma * np.std(polytrend)
    sigma_bounds = [polytrend + polytrend_std, polytrend - polytrend_std]

    sigma_idx = []
    for i in range(len(data)):
        if data[1][i] >= polytrend[i] + polytrend_std:
            sigma_idx.append(i)
        if data[1][i] <= polytrend[i] - polytrend_std:
            sigma_idx.append(i)

    data_sigma_clip = data.drop(labels=sigma_idx, axis=0, inplace=False).reset_index(drop=True)

    return sigma_idx, data_sigma_clip, polytrend, polytrend_std


ant_confirm_id = '1118060051368.dat'
ant_test_id = '1118060050249.dat'

dat = import_data(ant_confirm_id)

mag_dat = dat[1]
make_plot(mag_dat,
          fig_title=dat[0],
          plot_title='Magnitude',
          x_title='Modified Julian Day',
          y_title='Magnitude',
          mag=True,
          dynamic=True)

flux_dat = dat[2]
make_plot(flux_dat,
          fig_title=dat[0],
          plot_title='Flux',
          x_title='Modified Julian Day',
          y_title='Flux',
          mag=False,
          dynamic=True)

plot_mag_flux(mag_dat, flux_dat, fig_title=dat[0], dynamic=False)
