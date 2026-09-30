from Functions import *

Branch_Ratio_D = 1e-6

A_eff_string = "Average"

Cases = {
    "Average": (
        [1, 10, 1e3, 1e8],             # Overdensity
        [20, 90, 2.2e2, 1e3],             # x-position of BR labels
        [1, 1,  1.1, 0.8],            # y-position of BR labels
        [55, 57, 61, 55]                     # Rotations
    ),

    "Electron": (
        [8.5, 30, 1e3, 1e9],               # Overdensity
        [3, 30, 100, 8e2],               # m_pi_D / xpos
        [0.6, 1, 1.1, 0.8],              # xi / ypos
        [30, 55, 61, 55]                   # Rotations
    )
}

Overdensity_plot, xpos, ypos, Rotations = Cases[A_eff_string]

k_res = w_res = 100

with PdfPages("../PDFs/Eta - Plot.pdf") as pdf:
    fig, ax = plt.subplots(figsize=(6, 6))

    X = np.loadtxt(f"../Texts/X-{k_res}x{w_res}.csv", delimiter = " ")
    Y = np.loadtxt(f"../Texts/Y-{k_res}x{w_res}.csv", delimiter = " ")
    x, y = interpolate_function('../Texts/Bullet_Cluster - Copy.csv', True, 99, 0, 200)
    p, v = interpolate_function('../Texts/Relic_Density - Copy.csv', True, 10, 0, 200)

#Bullet
    Bullet_Cluster, = ax.plot(x, y, '--', color='black')
    ax.fill_between(x, y, 4.0375, where=(y <= 4.0375), color='gray', alpha=.6)
    ax.text(4, 2, "Bullet Cluster\nExcluded", ha="center", va="center", fontsize=14, color = "black", rotation = 8)

#Relic Density
    Relic_Density, = ax.plot(p, v, '--', color='blue')
    ax.fill_between(p, v, 4.0375, where=(v <= 4.0375), facecolor='lightblue', alpha = 0.4, edgecolor='blue', hatch='\\\\', linewidth=1)
    ax.text(3.5, 3.55, r"$(\Omega h^{2})_{\mathrm{th}}<0.12$", ha="center", va="center", fontsize=14, color = "blue", rotation = 22)

#Rho-Pi-Pi Cutoff
    Rho_Pi_Pi_Cutoff, = ax.plot([1, 2e3], [4.0375, 4.0375], color='maroon', linestyle='--')
    ax.axhspan(4.0375, 6, color='red', alpha=0.7)
    ax.text(4, 4.2, "$\\rho_D \\nrightarrow \\pi_D\\pi_D$", 
            ha="center", va="center", fontsize=16, color = "maroon")  
    
#Eqn 2 limit
    Cutoff, = ax.plot([1, 2e3], [0.4, 0.4], color='darkturquoise', linestyle='--')
    ax.axhspan(0, 0.4, color='darkturquoise', alpha=0.3)
    ax.text(9e2, 0.25, f"$\\xi$ < 0.4", ha="center", va="center", fontsize=14, color = "darkturquoise")


#Colors
    #cmap = matplotlib.colormaps.get_cmap(cmap_name)
    cmap = matplotlib.colormaps.get_cmap('tab10')
    n = len(Overdensity_plot)

    colors = [cmap(i) for i in range(n)]
    colors[3] = 'purple'

    legend_handles = []

    for idx, Xi_D in enumerate(Overdensity_plot):
        #if idx != 2:
        #    continue
        sigma_levels = [-2]
        fmt_dict = {-2: f"{Xi_D:.2e}"}
        N = np.loadtxt(f"../Texts/N_Xi={Xi_D:.2e}-0.01ev-{k_res}x{w_res}-BR={Branch_Ratio_D:.2e}-{A_eff_string}_A_eff.csv", delimiter = " ")   
        CS = ax.contour(X, Y, N, linestyles = "-", levels=sigma_levels, colors=[colors[idx]], linewidths=2)
        ax.text(xpos[idx], ypos[idx], f"$\\eta$ = {sci_label_unicode(float(fmt_dict[-2]), -1)}",  ha="center", va="center", fontsize=14, color = colors[idx], rotation = Rotations[idx])
        
    text = (f"BR = {sci_label_unicode(Branch_Ratio_D, -1)}\n$m_\\nu$ = 0.01eV")
    ax.text(2e2, 4.6, text, ha="left", va="center", fontsize=14, color = "white")
    ax.set_xlim(left=1 , right = 2e3)
    ax.set_ylim(bottom=0 , top=5)   
    ax.set_xlabel(r"$m_{\pi_D}$ [MeV]", size = 16)
    #ax.set_ylabel(r"$\zeta$", size = 14)
    ax.set_ylabel(r"$\xi = m_{\pi_D}/f_{\pi_D}$", size = 16)
    ax.set_xscale('log')
    plt.tick_params(direction="in",length=10,labelsize=16)
    plt.tick_params(which="minor",direction="in",length=4)
    plt.tick_params(axis='both', which='both', top=True, bottom=True, left=True, right=True)
    plt.tick_params(axis='x',pad=7)
    #plt.grid()
    pdf.savefig(bbox_inches="tight")
    plt.close()