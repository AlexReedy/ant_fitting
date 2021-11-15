from fittingLib_rt import *
fit = FittingLibrary(pause=.5)

ant_confirm_id = '1118060051368.dat'
ant_test_id = '1118060050249.dat'

fit.import_data(file=ant_test_id)

#fit.plot_mag(save=True, show=True)
#fit.plot_flux(save=True, show=True)
#fit.sigma_clipping()
#fit.plot_sigma_clip(save=True, show=True)
#fit.get_average()
#fit.plot_sigma_clip_avg()

fit.plot_mag_dynamic()
fit.plot_flux_dynamic()
fit.sigma_clipping()
fit.plot_sigma_clip_dynamic()



