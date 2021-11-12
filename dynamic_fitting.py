from antLib import *
lib = ant_fit()

ant_confirm_id = '1118060051368.dat'
ant_test_id = '1118060050249.dat'

lib.import_data(file=ant_confirm_id)
lib.sigma_clipping(5, 5)
lib.plot_sigma_clip(show_clipped=True)


