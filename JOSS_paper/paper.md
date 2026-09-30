---
title: 'PARVATI and SHIVA: A Python package and GUI for the computation and analysis of astronomical mean line profiles'
tags:
  - Python
  - astronomy
  - spectroscopy
  - mean line profiles
  - radial velocity
  - variability
authors:
  - name: Monica Rainer
    orcid: 0000-0002-8786-2572
    equal-contrib: true
    affiliation: 1
  - corresponding: true
affiliations:
 - name: INAF - Osservatorio Astronomico di Brera, Italy
   index: 1
date: 29 September 2026
bibliography: parvati.bib


# Summary

High-resolution spectroscopy is a powerful instrument to study the characteristics of astronomical objects, e.g., their physical parameters, chemical composition, radial velocity (RV), projected rotational velocity (vsini), and so on. The drawback is a lower Signal-to-Noise Ratio (SNR) compared to low-resolution spectroscopy, that hinders the study of faint signals. To overcome this limitation, mean line profiles are used in several astronomical fields (e.g., exoplanets search and characterization, asteroseismology, stellar kinematics) to combine the signal of hundreds or thousands of spectral lines in a single mean line with increased SNR.
PARVATI (Profiles Analysis and Radial Velocities using Astronomical Tools for Investigation) is a stand-alone Python package that contains several useful functions to create mean line profiles or extract single spectroscopic lines from the spectra. The line profiles may then be used to compute RVs, vsini, the equivalent widths (EW), the line moments, and other additional scientific information. It is complemented by SHIVA (a Simple and Helpful Interface for Variability Analysis), a standalone Python pyQT6 GUI wrapper for PARVATI.

# Statement of need

Mean line profiles are a powerful tool to study faint spectroscopic signals, such as the line profile variations due to non-radial pulsation modes, the radial velocity variations due to the Keplerian motion of a star-planet system, or the absorption due to the presences of atoms and molecules in the exoplanetary atmospheres. The profiles are obtained using the cross-correlation (CCF, `@Baranne:1996`, `@Pepe:2002`) or the least-squares deconvolution (LSD, `@Donati:1997`) of an observed spectrum with a spectral line mask. Typically the mask is a simple two-column list with the wavelengths and the depths of the spectral lines that will be used to compute the mean line profile, where the depths are used to weight the contribution of each line to the total profile. The SNR of the profile increases in first approximation with the square-root of the number of the lines used to create it: in the case of solar-like stars, this number is usually of the order of several thousands in the optical spectral range. 
With the plethora of high-resolution spectrographs used in the astronomical community, a flexible tool to compute mean line profiles from spectra with very different formats and spectral ranges, that allows the use of both standard and personalised masks is needed.
There is also a lack of public softwares to perform the next step of the mean line profiles’ analysis: despite the huge amount of information that can be obtained from the mean line profiles, many astronomers use them mainly to recover the quantities derived with a simple Gaussian fit (radial velocities, full-width-at-half-maximum, CCF contrast), with the only addition in some cases of the line bisector and the bisector’s span.

# State of the field

While the CCFs have been widely used in the last fifty years to measure radial velocities `[@Baranne:1979]`, and the LSD profiles have been used for more than twenty years in stellar variability studies `[@Donatib:1997]`, still there are only few codes publicly available dedicated to this work. Additionally, these codes are either quite old (LSD), or written in a proprietary language (iLSD, `@Kochukhov:2010`, or optimised for specific scientific cases (e.g., tayph, for the study of exoplanetary atmospheres, `@Hoeijmakers:2020`). 
The major high resolution optical spectrographs (e.g., HARPS, HARPS-N, ESPRESSO) are equipped with Data Reduction Softwares (DRS) that output not only the fully reduced spectra, but also their CCFs: unfortunately these DRS are mostly black-box programs that can hardly be customised by the visiting astronomers, and the available stellar masks’ libraries are usually very scarce. The latter point is a major problem because using a sub-optimal mask will hinder to possibility of looking for very faint signals: to better exploit the mean line profiles’ potentiality, the profiles should be created using masks that are optimised for the searched-for signal, i.e. masks where all and only the spectral lines present in the spectrum are listed, and their depths are correlated to the real line depths. As an alternative to the publicly available programs and the DRSs, many astronomers write their own private CCF or LSD code, that is usually suited to a specific scientific case or spectrograph.

# Software design

PARVATI is a simple Python package that may be directly installed with pip or downloaded from [GitHub](https://github.com/mrainer74/parvati).
It contains several independent functions, that may be divided in three main categories: (1) spectra ingestion and normalisation, (2) single line extraction or mean line profile computation (both as CCF and LSD), (3) line analysis. The line analysis functions enable to fit a single line or multiple lines simultaneously with many different fitting functions, to compute RVs, line widths and/or vsini, EWs, the line bisector and the bisector's span, the first five line moments (EW, RV, width, skewness and kurtosis), and to perform the Fourier transform of the line.
All the functions are highly customable, and may be integrated in any kind of personal workflow.

SHIVA is a GUI wrapper for PARVATI that allows to streamline the analysis process, from spectra ingestion up to the creation of time series with the physical quantities derived from the analysis, saving all main results as FITS files and (optionally) auxiliary ASCII files, and keeping a detailed log of the work done. It is freely avalaible on [GitHub](https://github.com/mrainer74/shiva), and it may be run simply by command line as:
```
python shiva.py
```

# Research impact statement
PARVATI is a small, light software that may be applied to every field of astronomy relying on high-resolution spectroscopy. It allows to conduct homogeneous analyses using different datasets, and it is ever evolving according to the requests of the community.
Up to now, PARVATI has been mainly used within the Italian exoplanetary and stellar community, but it has been presented to the wider astronomical community in international congresses (EAS 2021 Introducing a Python package for mean line profiles computation and analysis; Hors3s 2026, PARVATI and SHIVA New Tools for the Creation and Analysis of Mean Line Profiles). Up to the end of 2025, PARVATI was referenced either as a anonymous self-written code or with the working name of MANDALA, but the name was changed to avoid duplication in PyPI once the code was distributed as a Python package.
Some of the works in which PARVATI has been used include:
- the analysis of high-resolution near-infrared spectra of Mars: mean line profile creation, RVs, EWs and moments computation `[@Rainer:2026]`
- the analysis of high-resolution optical and near-infrared spectra of exoplanet-host stars:
   - EWs of single transmission lines of exoplanets orbiting the very active star V1298Tau (G. Guilluy, paper in preparation), 
   - mean line profile creation for a very fast rotating exoplanet-host star, profile fitting and RVs estimation (M.C. D'Arpa et al., paper under review)
   - mean line profile fitting, RV estimation, differential rotation investigation `[@Rainer:2021]`
A tight connection with several working groups with different scientific cases (e.g., search and characterization of exoplanets, kinematics of stars in globular clusters, asteroseismology) drives an ongoing update of PARVATI.


# AI usage disclosure

Generative AI tools were used only for a) a small sub-routine in PARVATI (find_shift_fft), where the AI Overview answer was used as it was, and b) to do the first rough translation of SHIVA from Tkinter (SHIVA '<' 3) to PyQT6 (SHIVA v3.x and onwards). No AI tools were used in the writing of this manuscript, or the preparation of supporting materials.

# References
