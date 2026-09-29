# Dark Rho Meson

## Overview

This repository contains Python code for calculating neutrino interactions with dark matter through a dark $\rho$ meson and studying their effects on the neutrino flux observed by IceCube-Gen2.

The code calculates the neutrino flux, interaction rates, and expected event rates for different dark matter overdensities, branching ratios, dark $\rho$ meson masses, and other model parameters.

## Structure

- `src/` — Core calculation functions
- `scripts/` — Scripts for running calculations and generating plots
- `data/` — Input data and experimental/effective-area tables
- `results/` — Generated numerical results
- `figures/` — Generated plots
- `requirements.txt` — Python package requirements.

## Calculations

- $m_\pi$ vs. $\eta$
- $m_\pi$ vs. $\mathrm{BR}$
- $\eta$ vs. $\mathrm{BR}$
- $\zeta$ vs. $\eta$
- $\zeta$ vs. $\mathrm{BR}$

## Requirements

- Python 3.12+
- Numpy 1.26.4
- Scipy 1.13.0
- Matplotlib 3.8.3
- Numba 0.66.0

Install the required packages with:

```bash
pip install -r requirements.txt
