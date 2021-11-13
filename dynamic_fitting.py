from fittingLib import *
fit = FittingLibrary(pause=.5)

for data_set in fit.data_sets:
    print(data_set)


ant_confirm_id = '1118060051368.dat'
ant_test_id = '1118060050249.dat'

fit.import_data(file=ant_test_id)

fit.plot_mag(save=True, show=True)
fit.plot_flux(save=True, show=True)

fit.sigma_clipping()
fit.plot_sigma_clip(save=True, show=True)



