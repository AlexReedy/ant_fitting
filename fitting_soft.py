import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def import_data(filename):
    data_path = os.path.abspath('/home/sedmdev/Research/ant_fitting/CRTS_Test_Data')

    data_set_path = os.path.join(data_path, filename)

    data = pd.read_csv(data_set_path, usecols=(0, 1, 2), delim_whitespace=True, header=None)
    data = data.sort_values(by=0, ascending=True, ignore_index=True)
    return data

mag_dat = import_data('1118060051368.dat')
flux_dat = import_data('1118060051368.dat')
flux_dat[1] = flux_dat[1].apply(lambda x: 3631.0 * (10.0 ** (-0.4 * x)))

fig, ax = plt.subplots(2)
fig.set_size_inches(10, 7)


ax[0].set_title('Magnitude Light Curve')
ax[0].set_xlabel('Modified Julian Day')
ax[0].set_ylabel('Magnitude')
ax[0].invert_yaxis()
ax[0].errorbar(mag_dat[0],
               mag_dat[1],
               yerr=mag_dat[2],
               linestyle='none',
               marker='s',
               ms=3,
               elinewidth=1,
               color='black')


ax[1].set_title(f'Flux Light Curve')
ax[1].set_xlabel('Modified Julian Day')
ax[1].set_ylabel('Flux')
ax[1].errorbar(flux_dat[0],
               flux_dat[1],
               linestyle='none',
               marker='s',
               ms=3,
               elinewidth=1,
               color='black')

fig.tight_layout()
plt.show()







