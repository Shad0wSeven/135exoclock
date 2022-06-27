from exotic.exotic import LimbDarkening
from exotic.api.elca import transit, lc_fitter
from ldtk.filters import create_tess
import matplotlib.pyplot as plt
import numpy as np



if __name__ == "__main__":
    z = np.loadtxt('210719.txt', delimiter=' ')
    

    for i in range(z.shape[0]):
        z[i][1] = 2 - z[i][1]
        
    prior = {
        'rprs': 0.1406,                               # Rp/Rs
        'ars': 5.61,                               # a/Rs
        'per': 1.4013795,                                # Period [day]
        'inc': 82.0,                                # Inclination [deg]
        'u0': 0, 'u1': 0, 'u2': 0, 'u3': 0,         # limb darkening (nonlinear)
        'ecc': 0,                                   # Eccentricity
        'omega': 120,                                 # Arg of periastron
        'tmid': z[0][0],                               # Time of mid transit [day],
        'a1': 0.9777,                                   # Airmass coefficients
        'a2': 0.0191,                                   # trend = a1 * np.exp(a2 * airmass)

        'teff':4984,
        'tefferr':117,
        'met': 0.020,
        'meterr': 0.130,
        'logg': 4.4102800, 
        'loggerr': 0.1075900
    }

    # example generating LD coefficients
    tessfilter = create_tess()

    ld_obj = LimbDarkening(
        teff=prior['teff'], teffpos=prior['tefferr'], teffneg=prior['tefferr'],
        met=prior['met'], metpos=prior['meterr'], metneg=prior['meterr'],
        logg=prior['logg'], loggpos=prior['loggerr'], loggneg=prior['loggerr'],
        wl_min=tessfilter.wl.min(), wl_max=tessfilter.wl.max(), filter_type="Clear")

    ld0, ld1, ld2, ld3, filt, wlmin, wlmax = ld_obj.nonlinear_ld()

    prior['u0'],prior['u1'],prior['u2'],prior['u3'] = [ld0[0], ld1[0], ld2[0], ld3[0]]

    # time = np.linspace(0.7, 0.8, 1000)  # [day]

    # simulate extinction from airmass
    # stime = time-time[0]
    # alt = 90 * np.cos(4*stime-np.pi/6)
    #airmass = 1./np.cos(np.deg2rad(90-alt))
    

    # GENERATE NOISY DATA
    # data = transit(time, prior)*prior['a1']*np.exp(prior['a2']*airmass)
    # data += np.random.normal(0, prior['a1']*250e-6, len(time))
    # dataerr = np.random.normal(300e-6, 50e-6, len(time)) + np.random.normal(300e-6, 50e-6, len(time))

    # add bounds for free parameters only
    mybounds = {
        'rprs': [0, 0.6],
        'tmid': [prior['tmid']-0.1, prior['tmid']+0.1],
        'ars': [1, 15],
        #'a2': [0, 0.3] # uncomment if you want to fit for airmass
        # never list 'a1' in bounds, it is perfectly correlated to exp(a2*airmass)
        # and is solved for during the fit
    }
    
    
    
    airmass = np.zeros(z[:, 0].shape)
    # myfit = lc_fitter(time, data, dataerr, airmass, prior, mybounds, mode='ns')
    myfit = lc_fitter(z[:, 0], z[:, 1], z[:, 2], airmass, prior, mybounds, mode='ns', verbose=True)
    

    for k in myfit.bounds.keys():
        print(f"{myfit.parameters[k]:.6f} +- {myfit.errors[k]}")

    fig, axs = myfit.plot_bestfit()
    plt.tight_layout()
    plt.show()

    fig = myfit.plot_triangle()
    plt.tight_layout()
    plt.show()