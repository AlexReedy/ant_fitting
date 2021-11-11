import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_dat(data_list, overlays=None):
    fig, ax = plt.subplots(1)
    fig.set_size_inches(10, 7)
    ax.set_title(f'Flux Light Curve')
    ax.set_xlabel('Modified Julian Day')
    ax.set_ylabel('Flux')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))

    if overlays is None:
        ax.errorbar(data_list[0][0],
                    data_list[0][1],
                    linestyle='none',
                    marker='s',
                    ms=3,
                    color='black')
        plt.show()

    if overlays != None:
        for i in range(overlays):
            ax.errorbar(data_list[i][0],
                        data_list[i][1],
                        linestyle='none',
                        marker='s',
                        ms=3,
                        color='black')
        plt.show()


def import_data(filename):
    data_path = os.path.abspath('/home/sedmdev/Research/ant_fitting/CRTS_Test_Data')

    data_set_path = os.path.join(data_path, filename)

    data = pd.read_csv(data_set_path, usecols=(0, 1, 2), delim_whitespace=True, header=None)

    mag_data = data.sort_values(by=0, ascending=True, ignore_index=True)

    flux_data = data.sort_values(by=0, ascending=True, ignore_index=True)
    flux_data[1] = flux_data[1].apply(lambda x: 3631.0 * (10.0 ** (-0.4 * x)))

    return filename, mag_data, flux_data


def plot_mag_flux(data1, data2, fig_title, dynamic=False, cool=False):
    fig, ax = plt.subplots(2)
    fig.set_size_inches(10, 7)
    fig.suptitle(f'CRTS {fig_title}')

    ax[0].set_title('Magnitude Light Curve')
    ax[0].set_xlabel('Modified Julian Day')
    ax[0].set_ylabel('Magnitude')
    ax[0].invert_yaxis()

    ax[1].set_title(f'Flux Light Curve')
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

    fig, ax = plt.subplots(1)
    fig.set_size_inches(10, 7)

    ax.set_title('Sigma Clipping')
    ax.set_xlabel('Modified Julian Day')
    ax.set_ylabel('Flux')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))

    ax.errorbar(data[0],
                data[1],
                linestyle='none',
                marker='s',
                ms=3,
                elinewidth=1,
                color='black')

    ax.plot(data[0],
            polytrend,
            linewidth=1,
            color='red')

    if not fill:
        ax.plot(data[0],
                polytrend + polytrend_std,
                linewidth=1,
                linestyle='--',
                color='black')

        ax.plot(data[0],
                polytrend - polytrend_std,
                linewidth=1,
                linestyle='--',
                color='black')

        plt.show()

    if fill:
        ax.plot(data[0],
                polytrend + polytrend_std,
                linewidth=1,
                linestyle='--',
                color='grey')

        ax.plot(data[0],
                polytrend - polytrend_std,
                linewidth=1,
                linestyle='--',
                color='grey')

        ax.fill_between(data[0],
                        sigma_bounds[0],
                        sigma_bounds[1],
                        color='whitesmoke')
        plt.show()

    return data_sigma_clip, polytrend, polytrend_std

ant_confirm_id = '1118060051368.dat'
dat = import_data('1118060050249.dat')
mag_dat = dat[1]
flux_dat = dat[2]

plot_mag_flux(mag_dat, flux_dat, fig_title=dat[0], dynamic=False)
sc_dat = sigma_clipping(flux_dat, 5, 5, fill=True)
