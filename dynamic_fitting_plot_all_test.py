from fittingLib import *
fit = FittingLibrary(pause=.1)

for data_set in fit.data_sets:
    print(data_set)
    fit.import_data(file=data_set)
    fit.plot_mag(save=True, show=True)
    fit.plot_flux(save=True, show=True)
    fit.sigma_clipping()
    fit.plot_sigma_clip(save=True, show=True)