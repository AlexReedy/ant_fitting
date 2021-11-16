from fittingLib_rt import *
import timeit
fit = FittingLibrary(pause=.5)

start = timeit.default_timer()
counter = 0
for data_set in fit.data_sets:
    ind_start = timeit.default_timer()
    fit.import_data(file=data_set)
    #fit.plot_mag(save=False, show=True)
    #fit.plot_flux(save=False, show=True)
    #fit.sigma_clipping()
    #fit.plot_sigma_clip(save=False, show=True)
    fit.plot_mag_dynamic()
    fit.plot_flux_dynamic()
    fit.sigma_clipping()
    fit.plot_sigma_clip_dynamic()
    ind_end = timeit.default_timer() - ind_start
    print(f'{data_set} [{counter} / {len(fit.data_sets)}] Completed:\n'
          f'Runtime: {int(ind_end)} sec\n'
          f'Moving to Next Data Set!')
    counter += 1
runtime = timeit.default_timer() - start

print(f'Total Runtime: {int(runtime)} sec')
