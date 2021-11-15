from fittingLib_rt import *
import timeit
fit = FittingLibrary(pause=.5)

start = timeit.default_timer()
counter = 0
for data_set in fit.data_sets:
    print(f'Completed: {counter} of {len(fit.data_sets)}')
    fit.import_data(file=data_set)
    #fit.plot_mag(save=False, show=True)
    #fit.plot_flux(save=False, show=True)
    #fit.sigma_clipping()
    #fit.plot_sigma_clip(save=False, show=True)
    fit.plot_mag_dynamic()
    fit.plot_flux_dynamic()
    fit.sigma_clipping()
    fit.plot_sigma_clip_dynamic()
    counter += 1
runtime = timeit.default_timer() - start
print(f'Runtime: {int(runtime)} seconds')
