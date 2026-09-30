from Functions import *
import sys

A_eff_string = sys.argv[1]
A_eff = globals()["A_eff_" + A_eff_string]
k_res = w_res = int(sys.argv[2])
M_Pi_plot = [float(sys.argv[3])]
Xi_plot = [float(sys.argv[4])]
start_time = time.time()

k = np.logspace(-15, 0, k_res)#BR
w = np.logspace(-3, 15, w_res) #Xi
X, Y = np.meshgrid(k, w)

np.savetxt(f"../results/BR-(Eta_vs_BR)-{k_res}x{w_res}.csv", X)
np.savetxt(f"../results/Eta-(Eta_vs_BR)-{k_res}x{w_res}.csv", Y)

x = np.loadtxt('../data/Flux vs Neutrino Energy Data.txt', delimiter = ",", usecols = 0)
x *= GeV

for idx, Xi_D in enumerate(Xi_plot):
    for idx, m_pi_D in enumerate(M_Pi_plot):

        N = np.zeros_like(X)
        N_att_grid = np.zeros_like(X)
        N_std_grid = np.zeros_like(X)
        st_dev = np.zeros_like(X)
        N_max = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                total_flux_unatt=np.zeros_like(x)
                total_flux_att=np.zeros_like(x)
                Branch_Ratio_D = X[i, j]
                Eta_D = Y[i, j]
                L = min((c / H_0) * (q * Eta_D)**-(1/3), max(Larray)) #cm
                L_grid = np.linspace(0, L, 1000)
                for mass in mass_L_array:

                    att_flux_integrand_vals = flux_integrand(True, Eta_D, z_L(L), zarray[:, None], mass, x[None, :] , Branch_Ratio_D, m_pi_D, Xi_D)
                    flux_att = trapezoid(att_flux_integrand_vals, zarray, axis = 0)    
                    total_flux_att += flux_att

                    unatt_flux_integrand_vals = flux_integrand(False, Eta_D, z_L(L), zarray[:, None], mass, x[None, :] , Branch_Ratio_D, m_pi_D, Xi_D)
                    flux_unatt = trapezoid(unatt_flux_integrand_vals, zarray, axis = 0)
                    total_flux_unatt += flux_unatt

                Phi = interp1d(x, (total_flux_unatt) / 3, kind='linear', fill_value = 0, bounds_error = False)
                Phi_mod = interp1d(x, (total_flux_att) / 3, kind='linear', fill_value = 0, bounds_error = False)

                E = np.min(x) * 2
                while E < np.max(x) / 2:
                    E_grid_temp = np.linspace(E / 2, E * 2, 1000)
                    integrand_vals = Integrand(E_grid_temp, A_eff, Phi)
                    result_unatt = cumulative_trapezoid(integrand_vals, E_grid_temp)[-1]
                    N[i, j] = 2 * np.pi * T * result_unatt
                    integrand_vals = Integrand(E_grid_temp, A_eff, Phi_mod)
                    result_att = cumulative_trapezoid(integrand_vals, E_grid_temp)[-1]
                    N_att_grid[i, j] = 2 * np.pi * T * result_att
                    st_dev[i, j] = np.sqrt(N[i, j])
                    N_std_grid[i, j] = ((N_att_grid[i, j] - N[i, j]) / (st_dev[i, j]))
                    if  N_std_grid[i, j] < N_max[i, j]:
                        N_max[i, j] = N_std_grid[i, j]
                    E *= Ice_Cube_res
    
        np.savetxt(f"../results/N_(Eta_vs_BR)_Contours-Xi={Xi_D:.2e}-M_pi={m_pi_D:.2e}-{k_res}x{w_res}.csv", N_max)

        print("Done with M_pi =", m_pi_D)
    print("Done with Xi = ", Xi_D)

elapsed_time = time.time() - start_time
print("Time Elapsed:", Elapsed_Time(elapsed_time))