from scipy.optimize import brentq
import numpy as np

M = 0.064      # eV
s = 7.5e-5      # eV^2
a = 2.46e-3     # eV^2

f = lambda m: m + np.sqrt(m**2 + s) + np.sqrt(m**2 + a) - M

m1 = brentq(f, 0, M)

m2 = np.sqrt(m1**2 + s)
m3 = np.sqrt(m1**2 + a)

print(m1, m2, m3, m1 + m2 + m3)