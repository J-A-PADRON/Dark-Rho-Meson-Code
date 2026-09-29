from Functions import *
import sys
#================================================================================= initialization ======================================================================
Xi_D = float(sys.argv[1])
Branch_Ratio_plot = [float(sys.argv[2])]
#Xi_D = 1
#Branch_Ratio_plot = [2.7e-7, 7e-7, 1e-5, 1e-2] #Electron
#Branch_Ratio_plot = [4.7e-7, 1e-6, 1e-5, 1e-2] #Average

"""Xi_D = 1e11
Branch_Ratio_plot = [3.3e-14, 8e-14, 1e-12, 1e-8] #Electron
#Branch_Ratio_plot = [5.2e-14, 1.2e-13, 1e-12, 1e-8] #Average"""

k_res = w_res = float(sys.argv[3])
A_eff = globals()[sys.argv[4]]

#====================================================================== plot Zeta vs m_pi_D with sigmas ==================================================================
start_time = time.time()

k = np.logspace(np.log10(0.01), np.log10(2000), k_res) #pion mass
w = np.logspace(np.log10(0.01), np.log10(6), w_res) #zeta
X, Y = np.meshgrid(k, w)

#print(k, w)
np.savetxt(f"../Texts/X-{k_res}x{w_res}.csv", X)
np.savetxt(f"../Texts/Y-{k_res}x{w_res}.csv", Y)

for idx, Branch_Ratio_D in enumerate(Branch_Ratio_plot):
    L = min((c / H_0) * (q * Xi_D)**-(1/3), max(Larray)) #cm
    L_grid = np.linspace(0, L, 1000)
    N = np.zeros_like(X)
    N_att_grid = np.zeros_like(X)
    N_std_grid = np.zeros_like(X)
    st_dev = np.zeros_like(X)
    N_max = np.zeros_like(X)
    N_events = []

    #i is zeta and j is the pion mass
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            total_flux_unatt=np.zeros_like(Neutrino_Energy_Range)
            total_flux_att=np.zeros_like(Neutrino_Energy_Range)
            m_pi_D = X[i, j]
            Zeta_D = Y[i, j]
            R_0 = 0
            for mass in mass_L_array:

                att_flux_integrand_vals = flux_integrand(True, Xi_D, z_L(L), zarray[:, None], mass, Neutrino_Energy_Range[None, :] , Branch_Ratio_D, m_pi_D, Zeta_D)
                flux_att = trapezoid(att_flux_integrand_vals, zarray, axis = 0)    
                total_flux_att += flux_att

                unatt_flux_integrand_vals = flux_integrand(False, Xi_D, z_L(L), zarray[:, None], mass, Neutrino_Energy_Range[None, :] , Branch_Ratio_D, m_pi_D, Zeta_D)
                flux_unatt = trapezoid(unatt_flux_integrand_vals, zarray, axis = 0)
                total_flux_unatt += flux_unatt

            Phi = interp1d(Neutrino_Energy_Range, (total_flux_unatt) / 3, kind='linear', fill_value = 0, bounds_error = False)
            Phi_mod = interp1d(Neutrino_Energy_Range, (total_flux_att) / 3, kind='linear', fill_value = 0, bounds_error = False)

            E = np.min(Neutrino_Energy_Range) * 2
            while E < np.max(Neutrino_Energy_Range) / 2:

                E_grid_temp = np.linspace(E / 2, E * 2, 1000)
                integrand_vals = Integrand(E_grid_temp, A_eff, Phi)
                result_unatt = trapezoid(integrand_vals, E_grid_temp)
                N[i, j] = 2 * np.pi * T * result_unatt

                if i == 0 and j == 0:
                    N_events.append((E / GeV, N[i, j]))

                integrand_vals = Integrand(E_grid_temp, A_eff, Phi_mod)
                result_att = trapezoid(integrand_vals, E_grid_temp)
                N_att_grid[i, j] = 2 * np.pi * T * result_att
                st_dev[i, j] = np.sqrt(N[i, j])
                N_std_grid[i, j] = ((N_att_grid[i, j] - N[i, j]) / (st_dev[i, j]))
                if  N_std_grid[i, j] < N_max[i, j]:
                    N_max[i, j] = N_std_grid[i, j]
                    #N_events[i, j] = N[i, j]
                E *= Ice_Cube_res
                #print(N[i, j])
            """if i == 0 and j == 0:
                    np.savetxt("../Texts/Events.txt", N_events, delimiter = ",")"""
            #print(f"Done with i = {i}, j = {j}")
    np.savetxt(f"../Texts/N_BR={Branch_Ratio_D:.2e}-0.01eV-{k_res}x{w_res}-Eta={Xi_D:.2e}-{str(A_eff)}_A_eff.csv", N_max)
    #np.savetxt(f"../Texts/N_BR={Branch_Ratio_D:.2e}-0.01eV-{k_res}x{w_res}-Eta={Xi_D:.2e}-Electron_A_eff.csv", N_max)
    #np.savetxt(f"../Texts/N_BR={Branch_Ratio_D:.2e}-0.01eV-{k_res}x{w_res}-Eta={Xi_D:.2e}-Average_A_eff.csv", N_max)

    print("Done with BR = ", Branch_Ratio_D)

elapsed_time = time.time() - start_time
print("Time Elapsed:", Elapsed_Time(elapsed_time))