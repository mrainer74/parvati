# PARVATI

PARVATI (Profiles Analysis and Radial Velocities using Astronomical Tools for Investigation) is a Python package for the analysis of astronomical spectra.

## Introduction
PARVATI contains several useful functions that allow to create mean line profiles or extract single spectroscopic lines from ASCII or FITS spectra. The line profiles may then be used to compute the radial velocities, the projected rotational velocities, the equivalent widths, the line moments, and other additional scientific information.
This README file will briefly cover all the available PARVATI functions, but a more detailed description of the functions and their input parameters may be obtained with:
```
import parvati as pa
help(pa)
help(pa.read_spectrum)
help(pa.FUNCTION)
```

PARVATI may be either downloaded from [GitHub](https://github.com/mrainer74/parvati) or installed using pip:
```
python -m pip install parvati
```

## Preparation of the spectra
The input spectra may have different formats: either ASCII files with wavelength, flux and additional information (e.g., SNR, errors, or echelle order number), standard monodimensional FITS files or FITS tables. The data in the FITS tables may be either in different fields of hdu[1] (like for GIANO-B ms1d data or ESPRESSO s1d data) or in different hdus (like in ESPRESSO s2d data).
The spectra may be read with the `read_spectrum` function.
Before extracting the line profiles they must be normalised, e.g., using the `norm_spectrum` function.

### Read the spectra
The function `read_spectrum` will require as input the filename of the spectrum, and accordingly to the other options given it will read:

- a monodimensional FITS file with the flux as the hdu[0].data and the wavelength in the hdu[0].header (CRVAL1, CDELT1, NAXIS1)
- a FITS file in the e2ds format of HARPS/HARPS-N/SOPHIE, with the echelle ordes still unmerged and the wavelength information in the header in the *DRS CAL TH DEG LL and *DRS CAL TH COEFF LLXX keywords
- a FITS table with all the data in hdu[1].data. By default, the wavelength will be read in the first field and the flux in the second field, but the number of the field may be specified. If there are any additional data as SNR and/or echelle order number and/or normalised flux and/or absolute errors, they may be specified here. If given, the S/N supersedes the errors, otherwise the errors will be transformed in S/N (S/N=flux/errors).
- a FITS table with data in several different hdu[X]. By default, the wavelength will be read in hdu[1] and the flux in the hdu[2], but the number of the hdus may be specified. If there are any additional data as SNR and/or echelle order number and/or normalised flux and/or absolute errors, they may be specified here. If given, the S/N supersedes the errors, otherwise the errors will be transformed in S/N (S/N=flux/errors).
- an ASCII files with at least two columns (wavelength and flux), but additional columns with SNR and/or echelle order number and/or normalised flux and/or absolute errors may be specified here. If given, the S/N supersedes the errors, otherwise the errors will be transformed in S/N (S/N=flux/errors). 

The wavelength is assumed to be in Angstroms and in vacuum, if otherwise then it must be specified using the `unit` and the `vacuum` parameters.

> [!IMPORTANT]
> The column/field(hdu numbers to use in the `read_spectrum` function start with 1, not 0

> [!TIP]
> Read the GIANO-B ms1d data with the options: wavecol=2, fluxcol=3, snrcol=4, echcol=1
> Read the ESPRESSO S1D data with the options: wavecol=1, fluxcol=3, errcol=4
> Read the ESPRESSO S2D data with the options: wavecol=4, fluxcol=1, errcol=2
> Read the CARMENES (VIS and NIR) data with the options: wavecol=4, fluxcol=1, errcol=3

### Normalise the spectra
If the spectra are not normalised, it is possible to use the function `norm_spectrum` to do so. The function requires at least the wavelength and flux as input. It is possible to set the degree of the polynomial and a number of subsets to be normalised independently.

If the `refine` option is set to `True`and either echelle orders or the subsets are given, then the normalisation may be refined by ensuring a smooth variation of the polynomial coefficients along the orders.

## Creation of the profiles
Once in possession of normalised spectra, the line profiles may be extracted or created in several different ways, as detailed below.

### Single line extraction
The function `extract_line` requires the spectrum in the format given by `read_spectrum` or `norm_spectrum`, the laboratory wavelength of the desired line, the radial velocity range and step of the extraction window. The extracted line will be interpolated on a Doppler velocity range, to help with the subsequent analysis.

### Mean line profile: LSD
The function `compute_lsd` compute the mean line profile by performing a Least-Squares Deconvolution (LSD) of the spectrum in the format given by `read_spectrum` or `norm_spectrum` with a mask that may be either an ASCII mask (VALD stellar mask, simple 2-columns file, normalised spectrum/model) or a FITS file (mask or normalised spectrum/model). Several options may be passed to optimised the profile extraction.

The LSD computation has been adapted from [Donati J.-F., et al., 1997, MNRAS 291, 658](https://doi.org/10.1093/mnras/291.4.658) and [Kochukhov O., et al., 2010, A&A 524, 5](https://doi.org/10.1051/0004-6361/201015429).

> [!IMPORTANT]
> To save computational time, the spectra should be split in subsets, and LSD profiles are computed for each subset independently and then averaged. This is naturally done using the echelle orders/subsets option in `norm_spectrum`: `compute_lsd` will automatically find the separations between the orders where the wavelength gap is larger than the average wavelength step or if there is overlapping.

### Mean line profile: CCF
The function `compute_ccf` compute the mean line profile by performing a Cross-Correlation of the spectrum in the format given by `read_spectrum` or `norm_spectrum` with a mask that may be either an ASCII mask (VALD stellar mask, simple 2-columns file, normalised spectrum/model) or a FITS file (mask or normalised spectrum/model). Several options may be passed to optimise the profile extraction.

> [!IMPORTANT]
> To save computational time, the spectra should be split in subsets, and CCF profiles are computed for each subset independently and then averaged. This is naturally done using the echelle orders/subsets option in `norm_spectrum`: `compute_ccf` will automatically find the separations between the orders where the wavelength gap is larger than the average wavelength step or if there is overlapping.

> [!WARNING]
> The cross-correlation with a spectrum is still unreliable

## Analysis of the profiles
Once the profiles have been obtained, PARVATI allows to perform several useful operations on the data, to better analyse them.

### Normalise the profiles
The profiles should already be normalised, but any slight deviation from a perfect normalisation of the original spectra will impact on the normalisation of the profiles. It is better to normalised them using the `norm_profile` function. 
This function requires as input NOT the name of a single file, but an ASCII file with a list of file names: this will allow to compute also an average mean line profile and the standard deviation of the profiles from this average, to better see where possible line profile variations are located. 
The input files may be either ASCII or FITS files with radial velocities, flux and (optional) errors. 

> [!TIP]
> It is possible to switch off the creation of the average mean line profile and standard deviation by using the parameter `std=None`

### Fit the profiles
Once normalised, the profiles may be fitted using the `fit_profile` function. It is possible to choose between different fitting functions: Gaussian, Asymmetric Gaussian, Supergaussian, Lorentzian, Voigt or rotational profile.
All the fitting functions yield a Radial Velocity (RV) estimation, the Equivalent Width (EW) and the width of the line, that will correspond either to the *v*sin*i* (for the rotational function) or to the Full-Width-at-Half-Maximum (FWHM, for all the other functions).
It is possible to fit more than one component simultaneously (e.g., in the case of spectroscopic binaries or multiple systems), and each component may have a different fitting function. In this case, using correct initial guess parameters is crucial.
If the value of the instrumental resolution is given, then the result will contain both the total convoluted profile and the deconvolved profile. The instrumental broadening is considered in an analytical way, describing it as a normalizad Gaussian with FWHM = c/resolution, where c is the speed of light in km/s.
> [!WARNING]
> The Supergaussian and the rotational functions will ignore the resolution value.

> [!NOTE]
> The rotational function is taken from [Gray, D. F. 2008, The Observation and Analysis of Stellar Photosphere](https://ui.adsabs.harvard.edu/link_gateway/2008oasp.book.....G/PUB_HTML).

> [!IMPORTANT]
> The `fit_profile` function was changed in PARVATI v2.0.0, and its inputs and outputs are not compatible with previous PARVATI versions.
> The output dictionary of the `fit_profile` function has a complex structure, see the detailed description using the command `help(pa.fit_profile)`

### Compute the line moments
The first five line moments may be computed from the (normalised) profiles using the `moments` function. The moments are:

- m0: EW
- m1: RV
- m2: sigma, from which also the FWHM is derived
- m3: from which the skewness is derived
- m4: from which the kurtosis is derived.

The definition for the moments is taken from [Briquet M. & Aerts C., 2003, A&A 398, 687](https://doi.org/10.1051/0004-6361:20021683), and the estimations of the errors from [Teague R., 2019, Res. Notes AAS 3, 74](https://doi.org/10.3847/2515-5172/ab2125).

### Compute the line's bisector
The function`bisector` computes both the bisector of the line and the bisector's span. The error computation and the definition of the bisector's span are taken from [Baştürk Ö., et al., 2011, A&A 535, 17](https://doi.org/10.1051/0004-6361/201117740).

### Compute the Fourier Transform of the line
The function `fourier` first symmetrises the line and then performs the Fourier Transform (FT) of the symmetrised line. The symmetrisation process yields another estimate of the RV (but without any associtated error), while the positions of the first 3 zeroes of the FT give information on the *v*sin*i* and the differential rotation IF the rotational broadening is the dominant line broadening effect.
The *v*sin*i* is derived using the empirical formula from [Dravins, D., Lindegren, L., & Torkelsson, U. 1990, A&A, 237, 137](https://articles.adsabs.harvard.edu/pdf/1990A%26A...237..137D).

> [!WARNING]
> If the rotational broadening is not the dominant effect, then the *v*sin*i* returned by the `fourier` function are wrong and should not be used.

## Test files
A couple of simple scripts are given in the `tests` directory along with two high-resolution spectra and two VALD stellar masks to guide in computing/extracting the line profiles and then analysing them.

## Graphical interface: SHIVA
The graphical interface of PARVATI is SHIVA (Simple and Helpful Interface for Variability Analysis). SHIVA may be downloaded from https://github.com/mrainer74/shiva

> [!CAUTION]
> At the moment, SHIVA does not allow to use all the options of PARVATI, and the graphical window is still not optimised. 
