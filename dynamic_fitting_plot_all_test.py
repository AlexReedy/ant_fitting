from fittingLib import *
import timeit
fit = FittingLibrary(pause=0)

start = timeit.default_timer()
counter = 0
for data_set in fit.data_sets:
    print(f'Completed: {counter} of {len(fit.data_sets)}')
    fit.import_data(file=data_set)
    fit.plot_mag(save=True, show=False)
    fit.plot_flux(save=True, show=False)
    fit.sigma_clipping()
    fit.plot_sigma_clip(save=True, show=False)
    counter += 1
runtime = timeit.default_timer() - start
print(f'Runtime: {int(runtime)} seconds')
