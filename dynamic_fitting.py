from fittingLib import *
fit = FittingLibrary()

ant_confirm_id = '1118060051368.dat'
ant_test_id = '1118060050249.dat'

fit.import_data(file=ant_confirm_id)

fit.plot_mag(save=False, show=True)
fit.plot_flux(save=False, show=True)

fit.sigma_clipping()

fit.plot_sigma_clip(save=False, show=True)
fit.plot_sigma_clip(save=False, show_clipped=True, show=True)


