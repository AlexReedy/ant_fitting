import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os



def import_data(filename, mag_to_flux=False):
    data_path = os.path.abspath('/home/sedmdev/Research/ant_fitting/CRTS_Test_Data')

    data_set_path = os.path.join(data_path, filename)

    data = pd.read_csv(data_set_path, usecols=(0, 1, 2), delim_whitespace=True, header=None)
    data = data.sort_values(by=0, ascending=True, ignore_index=True)

    if not mag_to_flux:
        return data, filename

    if mag_to_flux:
        data[1] = data[1].apply(lambda x: 3631.0 * (10.0 ** (-0.4 * x)))
        return data, filename


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

def sigma_clipping(data, poly_order, sigma):
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

    return data_sigma_clip, polytrend, polytrend_std


mag_dat = import_data('1118060051368.dat', mag_to_flux=False)
flux_dat = import_data('1118060051368.dat', mag_to_flux=True)


log = open(f'crts_{mag_dat[1]}_log.txt', 'w')

plot_mag_flux(data1=mag_dat[0], data2=flux_dat[0], fig_title=mag_dat[1])
sigma_clip = sigma_clipping(flux_dat[0], 5, 5)

print(flux_dat[0])
print(sigma_clip[0])

log.close()


