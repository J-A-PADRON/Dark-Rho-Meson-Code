from Functions import *
import sys
Overdensity_plot= [float(sys.argv[1])]
Branch_Ratio_D = float(sys.argv[2])
k_res = w_res = int(sys.argv[3])
A_eff_string = sys.argv[4]
A_eff = globals()["A_eff_" + A_eff_string]

#Average
#Overdensity_plot = [22.1, 22.2, 22.3, 22.4]

#Electron
#Overdensity_plot = [8.1, 8.2, 8.3, 8.4]

#Overdensity_plot = [5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 30, 1e3, 1e9]


#====================================================================== plot Zeta vs m_pi_D with sigmas ==================================================================
start_time = time.time()

k = np.logspace(np.log10(0.01), np.log10(2000), k_res) #pion mass
w = np.logspace(np.log10(0.01), np.log10(6), w_res) #zeta
X, Y = np.meshgrid(k, w)

#print(k, w)
np.savetxt(f"../Results/M_pi-{k_res}x{w_res}.csv", X)
np.savetxt(f"../Results/Xi-{k_res}x{w_res}.csv", Y)

x = np.loadtxt('../Data/Flux vs Neutrino Energy Data - Original.txt', delimiter = ",", usecols = 0)
x *= GeV

for idx, Eta_D in enumerate(Overdensity_plot):
    L = min((c / H_0) * (q * Eta_D)**-(1/3), max(Larray)) #cm
    L_grid = np.linspace(0, L, 1000)
    N = np.zeros_like(X)
    N_att_grid = np.zeros_like(X)
    N_std_grid = np.zeros_like(X)
    st_dev = np.zeros_like(X)
    N_max = np.zeros_like(X)

    #i is Xi and j is the pion mass
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            total_flux_unatt=np.zeros_like(x)
            total_flux_att=np.zeros_like(x)
            m_pi_D = X[i, j]
            Zeta_D = Y[i, j]
            R_0 = 0
            for mass in mass_L_array:

                att_flux_integrand_vals = flux_integrand(True, Eta_D, z_L(L), zarray[:, None], mass, x[None, :] , Branch_Ratio_D, m_pi_D, Zeta_D)
                flux_att = trapezoid(att_flux_integrand_vals, zarray, axis = 0)    
                total_flux_att += flux_att

                unatt_flux_integrand_vals = flux_integrand(False, Eta_D, z_L(L), zarray[:, None], mass, x[None, :] , Branch_Ratio_D, m_pi_D, Zeta_D)
                flux_unatt = trapezoid(unatt_flux_integrand_vals, zarray, axis = 0)
                total_flux_unatt += flux_unatt

            Phi = interp1d(x, (total_flux_unatt) / 3, kind='linear', fill_value = 0, bounds_error = False)
            Phi_mod = interp1d(x, (total_flux_att) / 3, kind='linear', fill_value = 0, bounds_error = False)

            E = np.min(x) * 2
            while E < np.max(x) / 2:

                E_grid_temp = np.linspace(E / 2, E * 2, 1000)
                integrand_vals = Integrand(E_grid_temp, A_eff, Phi)
                result_unatt = trapezoid(integrand_vals, E_grid_temp)
                N[i, j] = 2 * np.pi * T * result_unatt
                integrand_vals = Integrand(E_grid_temp, A_eff, Phi_mod)
                result_att = trapezoid(integrand_vals, E_grid_temp)
                N_att_grid[i, j] = 2 * np.pi * T * result_att
                st_dev[i, j] = np.sqrt(N[i, j])
                N_std_grid[i, j] = ((N_att_grid[i, j] - N[i, j]) / (st_dev[i, j]))
                if  N_std_grid[i, j] < N_max[i, j]:
                    N_max[i, j] = N_std_grid[i, j]
                E *= Ice_Cube_res

    np.savetxt(f"../Results/N_Eta_Contours-Eta={Eta_D:.2e}-BR={Branch_Ratio_D:.2e}-{k_res}x{w_res}.csv", N_max)
    
    print(f"Done with Eta = {Eta_D:.2e}")

elapsed_time = time.time() - start_time
print("Time Elapsed:", Elapsed_Time(elapsed_time))