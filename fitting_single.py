from fittingLib import *
fit = FittingLibrary(pause=.5)

ant_confirm_id = '1118060051368.dat'
ant_test_id = '1118060050249.dat'

fit.import_data(file=ant_confirm_id)

# fit.plot_mag(save=True, show=True)
# fit.plot_flux(save=True, show=True)

fit.sigma_clipping()
# fit.plot_sigma_clip(save=True, show=True)

fit.get_average()
# fit.plot_sigma_clip_avg(save=True, show=True)

fit.get_fit_parameters()
fit.plot_fitting_parameters(save=False)




