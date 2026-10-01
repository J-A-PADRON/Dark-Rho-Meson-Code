import numpy as np

# Given values
M = 0.064       # eV
delta_M_S_squared = 7.5e-5
delta_M_A_squared = 2.46e-3
print("M =", M, "eV")
print("s =", delta_M_S_squared, "eV^2")
print("a =", delta_M_A_squared, "eV^2")

coefficients = [
    3,
    -4*M,
    4*delta_M_S_squared - 2*M**2 + 2*delta_M_A_squared,
    4*M*(M**2 - delta_M_A_squared - 2*delta_M_S_squared),
    4*M**2*delta_M_S_squared - (M**2 - delta_M_A_squared)**2
]

roots = np.roots(coefficients)
for i, root in enumerate(roots, 1):
    print(f"Root {i}: {root}")