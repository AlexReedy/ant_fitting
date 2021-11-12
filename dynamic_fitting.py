from fittingLib import *
fit = FittingLibrary()

ant_confirm_id = '1118060051368.dat'
ant_test_id = '1118060050249.dat'

fit.import_data(file=ant_test_id)

fit.plot_mag(save=True)

fit.sigma_clipping(5, 5)

fit.plot_sigma_clip(show_clipped=True, save=True)


