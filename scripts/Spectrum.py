import sys
sys.path.append("../Source")
from Functions import *

Eta_D = 1
Branch_Ratio_plot = [1e-5]
M_Pi_plot = [5, 10, 20, 50]
Xi_plot = [0.5]

with PdfPages("../Figures/Fig1_Spectrum.pdf") as pdf:
    start_time = time.time()
    plt.figure(figsize=(6, 6))

#Auger
    x, y = interpolate_function('../Data/Auger - Spectrum.txt', True, 1e7, 0, 200)
    Auger, = plt.plot(x, y, '-', color="grey", linewidth=0)
    plt.fill_between(x, y, 1e-7, color = "black", alpha = 0.6)
    plt.text(1.5e9, 4.1e-8, "Pierre Auger", ha="center", va="center", fontsize=14, color = "black", rotation = 25)

#IceCube
    m, n = interpolate_function('../Data/IceCube - Spectrum.txt', True, 0, 0, 200)
    IceCube, = plt.plot(m, n, '-', color="grey", linewidth=0)
    y_interp = interp1d(x, y, bounds_error=False, fill_value=(y[0], y[-1]))(m)
    plt.fill_between(m, n, y_interp, color = "grey", alpha = 1)
    plt.text(2e8, 9.8e-9, "IceCube 12.6 years", ha="center", va="center", fontsize=14, color = "black", rotation = 16)
    
#IceCube Gen2
    x, y = interpolate_function('../Data/Gen2 - Radio_Prediction_Data - 27 AUG 2026.csv', True, 0, 0, 200)
    IceCube_Gen2, = plt.plot(x, y, linestyle = 'dotted', color="dimgrey", linewidth=2)
    plt.text(5e9, 3e-10, "IceCube-Gen2 Radio", ha="center", va="center", fontsize=14, color = "dimgrey", rotation = 0)

    x = np.loadtxt('../Data/Flux vs Neutrino Energy Data - Original.txt', delimiter = ",", usecols = 0)
    x *= GeV
    colors = ["black", "purple", "forestgreen", "blue", "saddlebrown", "red"]
    L = min((c / H_0) * (q * Eta_D)**-(1/3), max(Larray)) #cm

    for j, m_pi_D in enumerate(M_Pi_plot):
        Branch_Ratio_D = Branch_Ratio_plot[0]
        Xi_D = Xi_plot[0]
        total_flux_unatt = np.zeros_like(x)
        total_flux_att = np.zeros_like(x)
        for mass in mass_L_array:
            att_flux_integrand_vals = flux_integrand(True, Eta_D, z_L(L), zarray[:, None], mass, 
                                                     x[None, :] , Branch_Ratio_D, m_pi_D, Xi_D)
            flux_att = trapezoid(att_flux_integrand_vals, zarray, axis = 0)    
            total_flux_att += flux_att

            unatt_flux_integrand_vals = flux_integrand(False, Eta_D, z_L(L), zarray[:, None], mass, 
                                                       x[None, :] , Branch_Ratio_D, m_pi_D, Xi_D)
            flux_unatt = trapezoid(unatt_flux_integrand_vals, zarray, axis = 0)
            total_flux_unatt += flux_unatt
        BR_label = sci_label_unicode(Branch_Ratio_D, decimals=-1)
        Eta_label = sci_label_unicode(Eta_D, decimals=0)

        if j == 0:
            plt.plot(x / GeV, GeV * (x / GeV)**2 * total_flux_unatt / 3 , linestyle="-"
                    , color=colors[j], label = "SM", linewidth=3)
        
        plt.plot(x / GeV, GeV * (x / GeV)**2 * total_flux_att / 3 , linestyle="-"
                 , color=colors[j + 1], label=f"$m_{{\\pi_D}}$ = {m_pi_D} MeV", linewidth=2, alpha = 0.7)
    
    constants = f"$\\xi$ = {Xi_D}\n$m_\\nu = 0.01\\,$eV\nBR = {BR_label}"
    plt.text(0.70, 0.7, constants, transform=plt.gca().transAxes, ha="left", va="top", fontsize=14)

    plt.ylim(bottom=1e-11, top=1e-7)
    plt.xscale('log')
    plt.xlabel('Neutrino Energy [GeV]', size = 16)
    plt.yscale('log')
    plt.ylabel(r"$E^2\Phi\;[\mathrm{GeV\,cm^{-2}\,s^{-1}\,sr^{-1}}]$", size = 16)

    plt.xlim(left = 1e7, right = 1e11)
    plt.legend(loc="center right", bbox_to_anchor=(0.95, 0.18), framealpha=0.5,
                borderaxespad=0., handlelength=1.5, fontsize = 12)
    plt.tick_params(direction="in", length=10, labelsize=16)
    plt.tick_params(which="minor", direction="in", length=4)
    plt.tick_params(axis='both', which='both', top=True, bottom=True, left=True, right=True)
    plt.tick_params(axis='x',pad=7)
    pdf.savefig(bbox_inches="tight")
    plt.close()

    elapsed_time = time.time() - start_time
    print("Flux vs Neutrino Energy Time:", Elapsed_Time(elapsed_time))