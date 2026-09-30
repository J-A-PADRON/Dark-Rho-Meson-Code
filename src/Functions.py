import time
import subprocess
import sys
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, LogFormatterMathtext
from scipy.integrate import cumulative_trapezoid
from scipy.integrate import trapezoid
from scipy.interpolate import interp1d
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D
import matplotlib
from pathlib import Path
from numba import njit
import math
#================================================================================= initialization ======================================================================
GeV = 1e3
MeV = 1
eV = 1e-6
cm = 1
fm = 1e-13 * cm
h_bar_c = 197.327 * MeV * fm # Gev * cm
q = 1
Omega_m = 0.315
Omega_l = 0.685
H_0 = 2.268e-18 #s^-1
c = 29979245800 #cm/s
R_1 = [0.01, 0.3, 0.8, 0.95]
n_nu_0 = 56 #cm^-3
g_rho_pi_pi = 6
T = 315360000 #sec (10 years)
eta = 3
epsilon = 0.07
gamma = -1

#No exponents, fine tuning
"""E_muon = 8.7e14
E_neut = 1.9e13
L_muon = 5.8e-62
L_neut = 2e-59"""

E_muon = 2.1e14
E_neut = 2.9e13
L_muon = 6.1e-61
L_neut = 4.3e-60

Old_Energy, Old_A_eff_Array = np.loadtxt('../Texts/Gen2_effective_areas.txt', delimiter = ",", unpack = True)
A_eff_Old = interp1d(Old_Energy, Old_A_eff_Array, kind='linear', fill_value = 0, bounds_error = False) #Original file with x already in units of log10(eV)

Electron_Energy, Electron_A_eff_Array = np.loadtxt('../Texts/Gen2_effective_areas - Electron - 27 AUG 2026.txt', delimiter = ",", unpack = True)
A_eff_Electron = interp1d(np.log10(Electron_Energy * (GeV / eV)), Electron_A_eff_Array, kind='linear', fill_value = 0, bounds_error = False)

Muon_Energy, Muon_A_eff_Array = np.loadtxt('../Texts/Gen2_effective_areas - Muon - 27 AUG 2026.txt', delimiter = ",", unpack = True)
A_eff_Muon = interp1d(np.log10(Muon_Energy * (GeV / eV)), Muon_A_eff_Array, kind='linear', fill_value = 0, bounds_error = False)

Tau_Energy, Tau_A_eff_Array = np.loadtxt('../Texts/Gen2_effective_areas - Tau - 27 AUG 2026.txt', delimiter = ",", unpack = True)
A_eff_Tau = interp1d(np.log10(Tau_Energy * (GeV / eV)), Tau_A_eff_Array, kind='linear', fill_value = 0, bounds_error = False)

A_eff_E_Range = np.logspace(16, 20, 200) #eV
A_eff_Average = interp1d(np.log10(A_eff_E_Range),(A_eff_Electron(np.log10(A_eff_E_Range)) 
                + A_eff_Muon(np.log10(A_eff_E_Range)) + A_eff_Tau(np.log10(A_eff_E_Range))) / 3, 
                kind='linear', fill_value=0, bounds_error=False)

Neutrino_Energy_Range = np.loadtxt('../Texts/Flux vs Neutrino Energy Data.txt', delimiter = ",", usecols = 0)
Neutrino_Energy_Range *= GeV

delta_M_S_squared = 7.5e-5 * (eV)**2 #MeV^2
delta_M_A_squared = 2.46e-3  * (eV)**2 #MeV^2
Ice_Cube_res = 1.1
M_L = 0.01 * eV #MeV
M_M = 0.05 * eV #MeV
M_H = 0.5 * eV #MeV
Larray = np.loadtxt("../Texts/L_array.txt")
zarray = np.logspace(-7,np.log10(1100),1000)
z_L = interp1d(Larray, zarray, kind='linear', bounds_error = False, fill_value='extrapolate')

@njit(cache=True, fastmath=True)
def M_2(M_1):
    return np.sqrt((M_1)**2 + delta_M_S_squared)
@njit(cache=True, fastmath=True)
def M_3(M_1):
    return np.sqrt((M_1)**2 + delta_M_S_squared + delta_M_A_squared)
mass_L_array = [M_L, M_2(M_L), M_3(M_L)]
mass_M_array = [M_M, M_2(M_M), M_3(M_M)]
mass_H_array = [M_H, M_2(M_H), M_3(M_H)]
Neutrino_Mass_Equations = [lambda x: x, M_2, M_3]
mass_arrays = [mass_L_array, mass_M_array, mass_H_array]
def sci_label_unicode(x, decimals=1):

    if x == 0:
        return "0"

    exponent = int(math.floor(math.log10(abs(x))))
    base = x / 10**exponent
    superscripts = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
    exp_str = str(exponent).lstrip("+").translate(superscripts)

    if 1 <= abs(x) < 10:
        if decimals == -1:
            return f"{x:.0f}"
        return f"{x:.{decimals}f}"

    if decimals == -1:
        return f"10{exp_str}"
    
    base_str = f"{base:.{decimals}f}"

    return f"{base_str}×10{exp_str}"
def Elapsed_Time(time):
    total_seconds = int(time)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"
def interpolate_function(data_file, use_log=False, x_start_offset=0, x_end_offset=0, num_points=100):
    x, y = np.loadtxt(data_file, delimiter=",", unpack=True)
    interpolator = interp1d(x, y, kind="linear", fill_value="extrapolate")

    xmin = x.min() - x_start_offset
    xmax = x.max() - x_end_offset

    if use_log:
        if xmin <= 0:
            raise ValueError("Logarithmic spacing requires xmin > 0.")
        x_new = np.logspace(np.log10(xmin), np.log10(xmax), num_points)
    else:
        x_new = np.linspace(xmin, xmax, num_points)

    y_new = interpolator(x_new)
    return x_new, y_new
def Integrand(E, Area, Phi):
    #100**2 [cm^2 / m^2] * Area(np.log10(E[MeV] / 1e-6[eV / MeV])) [m^2] * Phi(E) [MeV^-1 ....]
    return 100**2 * Area(np.log10(E / eV)) * Phi(E) #[cm * [MeV^-1 ....]]
@njit(cache=True, fastmath=True)
def m_rho(m_pi, Xi):
    return (m_pi * 2 * 0.57) / (-7.79 + np.sqrt(7.79**2 + 4 * 0.57 * Xi))
@njit(cache=True, fastmath=True)
def Gamma_rho(m_pi, Xi):
    return ((g_rho_pi_pi**2 / (6 * np.pi * m_rho(m_pi, Xi)**2)) * ((m_rho(m_pi, Xi)**2 - 4 * m_pi**2) / 4)**(3/2))
@njit(cache=True, fastmath=True)
def E_res(L, redshift, mass, m_pi, Xi):
    return (m_rho(m_pi, Xi) )**2 / (2 * (mass) * (1 + redshift(L)))
@njit(cache=True, fastmath=True)
def s(mass, energy, redshift):
    return 2 * mass * energy * (1 + redshift)
@njit(cache=True, fastmath=True)
def sigma(mass, energy, redshift, Branch_Ratio, m_pi, Xi):
    return (h_bar_c**2 * ((48 * np.pi * s(mass, energy, redshift) * Gamma_rho(m_pi, Xi)**2 * Branch_Ratio)
            / (m_rho(m_pi, Xi)**2 * ((s(mass, energy, redshift) - m_rho(m_pi, Xi)**2)**2 
            + (s(mass, energy, redshift)**2 * Gamma_rho(m_pi, Xi)**2) / (m_rho(m_pi, Xi)**2)))))
@njit(cache=True, fastmath=True)
def n_nu(Eta, redshift):
    return Eta * n_nu_0 * (1 + redshift)**3
@njit(cache=True, fastmath=True)
def lambda_(redshift, mass, energy, m_pi, Xi, Eta, Branch_Ratio):
    return 1 / (sigma(mass, energy, redshift, Branch_Ratio, m_pi, Xi) * n_nu(Eta, redshift))
@njit(cache=True, fastmath=True)
def exp_integrand(L, redshift, mass, energy, m_pi, Xi, Eta, Branch_Ratio):
    return 1 / lambda_(redshift(L), mass, energy, m_pi, Xi, Eta, Branch_Ratio)
@njit(cache=True, fastmath=True)
def H_z(redshift):
    return np.sqrt(H_0**2 * (Omega_m * (1 + redshift)**3 + Omega_l)) #s^-1
def H_AGN(redshift):
    return np.piecewise(
        redshift,
        [
            redshift <= 1.7,
            (redshift > 1.7) & (redshift < 2.7),
            redshift >= 2.7
        ],
        [
            lambda z: (1 + z)**5,
            2.7**5,
            lambda z: 2.7**5 * 10**(0.43*(2.7-z))
        ]
    )
def Luminosity(redshift, energy):
    return ((L_muon * ((energy * (1 + redshift) / (epsilon * E_muon))**(gamma)) 
            * np.exp(-(energy * (1 + redshift) / (epsilon * E_muon))**0.48))#big hump
            + (L_neut * ((energy * (1 + redshift) / (epsilon * E_neut))**(gamma)) 
            * np.exp(-(energy * (1 + redshift) / (epsilon * E_neut))**3.5)))
def flux_integrand(attenuate, Eta, z_, redshift, mass, energy, Branch_Ratio, m_pi, Xi):
    base = (c * (eta / (4 * np.pi * epsilon))
            * (1 / H_z(redshift))
            * H_AGN(redshift)
            * Luminosity(redshift, energy))
    if not attenuate:
        return base
    z = np.logspace(-7, np.log10(z_), 1000) #redshifts up to the cloud
    integrand = (c * n_nu(Eta, z[:, None])
                 * sigma(mass, energy, z[:, None], Branch_Ratio, m_pi, Xi)
                 / H_z(z[:, None])) #integrand up to the edge of cloud
    tau_curve = cumulative_trapezoid(integrand, z, axis = 0, initial=0) #evaluate only from 0 to the edge of cloud 
    #redshift = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #z = [1, 2, 3, 4, 5]
    #tau_curve = [tau(z(0)), ...., tau(z(4))]
    z_eval = np.minimum(redshift, z_) #replace everything above z_L with z_ in redshift (source redshifts)
    #z_eval =[1, 2, 3, 4, 5, 5, 5, 5, 5, 5]
    idx = np.searchsorted(z, z_eval) #find index of each value in z_eval so that the indices stay sorted and return an array of those indices
    #idx = [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4]
    idx = np.minimum(idx, len(z)-1) #checks to make sure indices dont go over the max length of z
    #tau = tau_curve[[0, 1, 2, 3, 4, 4, 4, 4, 4, 4]] 
    #= [tau(z(0)), tau(z(1)), tau(z(2)), tau(z(3)), tau(z(4)), tau(z(4)), tau(z(4)), tau(z(4)), tau(z(4)), tau(z(4))]
    tau = tau_curve[idx[:, 0], :]
    return base * np.exp(-tau)