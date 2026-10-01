# Dark Rho Meson

## Overview

This repository contains Python code for calculating neutrino interactions with dark matter through a dark $\rho$ meson and studying their effects on the neutrino flux observed by IceCube-Gen2.

The code calculates the neutrino flux and expected events for different neutrino overdensities, branching ratios (${\rm BR}(\rho_D\to\nu\bar{\nu}$)), $m_\pi$, $\xi$, $m_\nu$, $\rm{E^2}\Phi$ and Energy. This code is used to create the figures in https://arxiv.org/abs/2609.24887.

## Structure

- `src/` — Core calculation functions
- `scripts/` — Scripts for running calculations and generating plots
- `data/` — Input data/limits
- `results/` — Generated numerical results
- `figures/` — Generated plots
- `requirements.txt` — Python package requirements.

## Calculations

- Spectrum - $\rm{E^2}\Phi$ vs Energy
- ${\rm BR}(\rho_D\to\nu\bar{\nu}$) and $\eta$ Contours - $\xi$ vs $m_\pi$
- $\eta$ vs $m_\nu$
- $\eta$ vs ${\rm BR}(\rho_D\to\nu\bar{\nu}$)

## Requirements
These versions were the versions used at the time our plots were created.
- Python 3.12.10
- Numpy 1.26.4
- Scipy 1.13.0
- Matplotlib 3.8.3
- Numba 0.66.0

Install the required packages with:

```bash
pip install -r requirements.txt
