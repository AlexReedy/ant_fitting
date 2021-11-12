import antLib as lib

ant_confirm_id = '1118060051368.dat'
ant_test_id = '1118060050249.dat'

dat = lib.import_data(ant_confirm_id)

mag_dat = dat[1]
lib.make_plot(mag_dat,
              fig_title=dat[0],
              plot_title='Magnitude',
              x_title='Modified Julian Day',
              y_title='Magnitude',
              mag=True,
              dynamic=False)

flux_dat = dat[2]
lib.make_plot(flux_dat,
              fig_title=dat[0],
              plot_title='Flux',
              x_title='Modified Julian Day',
              y_title='Flux',
              mag=False,
              dynamic=True)
