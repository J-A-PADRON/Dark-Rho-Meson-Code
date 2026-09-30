from Functions import *

Xi_D = 1e9
Branch_Ratio_D = 1e-12
k_res = w_res = 100
Z_plot = [1]
    
start_time = time.time()

w = np.logspace(-9, -6, k_res)#m_nu [MeV]
k = np.logspace(np.log10(0.01), np.log10(5e2), w_res) #m_pi [MeV]
X, Y = np.meshgrid(k, w)

np.savetxt(f"../Texts/M_nu-(M_nu vs M_pi)-{k_res}x{w_res}.csv", Y)
np.savetxt(f"../Texts/M_pi-(M_nu vs M_pi)-{k_res}x{w_res}.csv", X)

x1, y1 = Open_Data('../Texts/Gen2_effective_areas.txt') # np.log10(E [eV]), m^2
x, y = interpolate_function('../Texts/Flux vs Neutrino Energy Full Data.txt', True, 0, 0, 200)
A_eff = interp1d(x1, y1, kind='linear', fill_value = 0, bounds_error = False)
x *= GeV

legend_handles = []
index = 0
for idx, Zeta_D in enumerate(Z_plot):
    N = np.zeros_like(X)
    N_att_grid = np.zeros_like(X)
    N_std_grid = np.zeros_like(X)
    st_dev = np.zeros_like(X)
    N_max = np.zeros_like(X)
    E_res_D = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            total_flux_unatt=np.zeros_like(x)
            total_flux_att=np.zeros_like(x)
            mass_D = Y[i, j]
            m_pi_D = X[i, j]
            L = min((c / H_0) * (q * Xi_D)**-(1/3), max(Larray))
            L_grid = np.linspace(0, L, 1000)
            R_0 = 0
            for equation in Neutrino_Mass_Equations:
                mass = equation(mass_D)
                
                att_flux_integrand_vals = flux_integrand(True, Xi_D, z_L(L), zarray[:, None], mass, x[None, :] , Branch_Ratio_D, m_pi_D, Zeta_D)
                flux_att = trapezoid(att_flux_integrand_vals, zarray, axis = 0)    
                total_flux_att += flux_att

                unatt_flux_integrand_vals = flux_integrand(False, Xi_D, z_L(L), zarray[:, None], mass, x[None, :] , Branch_Ratio_D, m_pi_D, Zeta_D)
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

    np.savetxt(f"../Texts/N_(M_nu vs M_pi)-(Zeta vs Eta vs BR)={Zeta_D:.2e}-{Xi_D:.2e}-{Branch_Ratio_D:.2e}-0.01eV-{k_res}x{w_res}-Eta={Xi_D:.2e}-New.csv", N_max)
print("Done with Zeta = ", Zeta_D)


elapsed_time = time.time() - start_time
print("Time Elapsed:", Elapsed_Time(elapsed_time))