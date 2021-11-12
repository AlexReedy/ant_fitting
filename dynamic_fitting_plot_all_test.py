from fittingLib import *
fit = FittingLibrary()

ant_confirm_id = '1118060051368.dat'
ant_test_id = '1118060050249.dat'

data_list = [ant_confirm_id, ant_test_id]

for i in range(len(data_list)):
    fit.import_data(file=data_list[i])

    fit.plot_mag(save=False)

    fit.sigma_clipping(5, 5)

    fit.plot_sigma_clip(show_clipped=True, save=True)