import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

import os, sys

#import parvati as pa
import sys
sys.path.append("/home/monica/Documents/GitHub/parvati/src/parvati")
import new_parvati as pa

testccf = 'fast_rotator_ccf.prf'
    
rv0 = -20
width = 100
    
outpng_fit = 'fast_rotator_ccf_fit.png'
outpng_bis = 'fast_rotator_ccf_bis.png'
outpng_fou = 'fast_rotator_ccf_fourier.png'
    

### Read the ASCII file with the profile

print('Normalising the profile')
norccf = pa.norm_profile(testccf, rvcol=1, prfcol=2, errcol=3, sfx='pfn', std=None, limits=False)

rvs = norccf[0][0]['rv_range']
flux = norccf[0][0]['nprofile']
errs = norccf[0][0]['error']


### Fit the profile with the correct linear limb darkening
### Other options:
### rv0= guess value of the center of the line
### width= guess value of the width of the line

gauss = pa.fit_profile(rvs, flux, errs=errs, ld=0.53, width=width, rv0=rv0)
rotational = pa.fit_profile(rvs, flux, errs=errs, ld=0.53, width=width, rv0=rv0, fit='r')
asymmetric = pa.fit_profile(rvs, flux, errs=errs, ld=0.53, width=width, rv0=rv0, fit='a')
supergaussian = pa.fit_profile(rvs, flux, errs=errs, ld=0.53, width=width, rv0=rv0, fit='s')
lorentzian = pa.fit_profile(rvs, flux, errs=errs, ld=0.53, width=width, rv0=rv0, fit='l')
voigt = pa.fit_profile(rvs, flux, errs=errs, ld=0.53, width=width, rv0=rv0, fit='v')

plt.xlabel('Doppler velocity (km/s)')
plt.ylabel('Normalised flux')
plt.plot(rvs, flux, 'k-', label='Mean profile')
plt.plot(rvs, gauss['profile'], 'C0', label='Gaussian fit')
plt.plot(rvs, rotational['profile'], 'C1', label='Rotational fit')
plt.plot(rvs, asymmetric['profile'], 'C0', label='Asymmetric Gaussian fit')
plt.plot(rvs, supergaussian['profile'], 'C0', label='Supergaussian fit')
plt.plot(rvs, lorentzian['profile'], 'C1', label='Lorentzian fit')
plt.plot(rvs, voigt['profile'], 'C1', label='Voigt fit')
plt.legend(loc='best')
plt.savefig(outpng_fit)
plt.show()
plt.close()

print(f"Gaussian fit: RV = {gauss[0]['gaussian']['rv']} +/- {gauss[0]['gaussian']['e_rv']}")
print(f"Rotational fit: RV = {rotational[0]['rotational']['rv']} +/- {rotational[0]['rotational']['e_rv']}")

### Compute first four moments of the line
moments = pa.moments(rvs, flux, errs=errs)
print(moments)
print(f"Moments: RV = {moments['m1']} +/- {moments['e_m1']}")

### Compute the bisector of the line
bis = pa.bisector(rvs, flux, errs=errs)

plt.plot(rvs, flux, 'k-', label='Mean profile')
plt.plot(bis['bisvel'], bis['bisflux'], 'C0', label='Line bisector')
plt.legend(loc='best')
plt.savefig(outpng_bis)
plt.show()
plt.close()


### Compute the Fourier transform
fft_res = pa.fourier(rvs, flux, errs=errs, ld=0.53, limits=(-149,104))

print(f"Rotational fit: vsini = {rotational[0]['rotational']['width']} +/- {rotational[0]['rotational']['e_width']}")
print(f"Result from first zero: {fft_res['vsini'][0]} +/- {fft_res['e_vsini'][0]}")
print(f"Result from second zero: {fft_res['vsini'][1]} +/- {fft_res['e_vsini'][1]}")
print(f"Result from third zero: {fft_res['vsini'][2]} +/- {fft_res['e_vsini'][2]}")

print(f"Result from all zero: {fft_res['mean_vsini']} +/- {fft_res['e_mean_vsini']}")
print(f"q2/q1 ratio: {fft_res['ratio']} +/- {fft_res['e_ratio']}")
print(f"RV from Fourier: {fft_res['rv']}")

plt.xlim(0,0.03)
plt.ylim(10**(-9),1)
plt.xlabel("Frequency [s/km]")
plt.ylabel("Fourier Amplitude")
plt.plot(fft_res['FFT_fr'],fft_res['FFT_pow'], label='Fourier transform')
plt.axhline(fft_res['FFT_err'], color='C1', label='White noise level')
plt.gca().set_yscale('log')
plt.legend(loc='best')
plt.savefig(outpng_fou)
plt.show()
plt.close()


