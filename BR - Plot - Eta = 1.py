from Functions import *

#================================================================================= initialization ======================================================================

Eta_D = 1
A_eff = "Average"

Cases = {
    (1, "Average"): (

        [4.7e-7, 1e-6, 4e-6, 1e-4],     # Branching ratios
        [30, 6, 1.3e2, 4e2],             # x-position of BR labels
        [1.3, 0.9, 1.1, 1.1],            # y-position of BR labels
        [60, 33, 55, 55]                 # rotation of BR labels

    ),

    (1, "Electron"): (
        [2.7e-7, 7e-7, 1e-5, 1e-2],
        [4, 38, 1.8e2, 7e2],
        [0.75, 0.9, 1.1, 0.8],
        [37, 55, 61, 55]
    ),

    (1e11, "Average"): (
        [5.2e-14, 2.4e-13, 1e-12, 1e-8],
        [18, 3.1, 1.3e2, 9e2],
        [1, 0.71, 1.1, 0.8],
        [55, 33, 61, 55]
    ),

    (1e11, "Electron"): (
        [3.3e-14, 8e-14, 1e-12, 1e-8],
        [3, 27, 1.3e2, 9e2],
        [0.71, 0.9, 1.1, 0.8],
        [35, 55, 61, 55]
    )
}

Branch_Ratio_plot, xpos, ypos, Rotations = Cases[(Eta_D, A_eff)]

Ice_Cube_res = 1.05
k_res = w_res = 300

with PdfPages("../PDFs/BR - Plot.pdf") as pdf:
    fig, ax = plt.subplots(figsize=(6, 6))

    X = np.loadtxt(f"../Texts/X-{k_res}x{w_res}.csv", delimiter = " ")
    Y = np.loadtxt(f"../Texts/Y-{k_res}x{w_res}.csv", delimiter = " ")
    x, y = interpolate_function('../Texts/Bullet_Cluster - Copy.csv', True, 99, 0, 200)
    p, v = interpolate_function('../Texts/Relic_Density - Copy.csv', True, 10, 0, 200)

#Bullet
    Bullet_Cluster, = ax.plot(x, y, '--', color='black')
    ax.fill_between(x, y, 4.0375, where=(y <= 4.0375), color='gray', alpha=.6)
    ax.text(4, 1.5, "Bullet Cluster\nExcluded", ha="center", va="center", fontsize=14, color = "black", rotation = 8)

#Relic Density
    Relic_Density, = ax.plot(p, v, '--', color='blue')
    ax.fill_between(p, v, 4.0375, where=(v <= 4.0375), facecolor='lightblue', alpha = 0.4, edgecolor='blue', hatch='\\\\', linewidth=1)
    ax.text(3.5, 3.43, r"$(\Omega h^{2})_{\mathrm{th}}<0.12$", ha="center", va="center", fontsize=14, color = "blue", rotation = 35)

#Rho-Pi-Pi Cutoff
    Rho_Pi_Pi_Cutoff, = ax.plot([1, 2e3], [4.0375, 4.0375], color='maroon', linestyle='--')
    ax.axhspan(4.0375, 6, color='red', alpha=0.7)
    ax.text(4, 4.2, "$\\rho_D \\nrightarrow \\pi_D\\pi_D$", 
            ha="center", va="center", fontsize=16, color = "maroon")  

#Eqn 2 limit
    Cutoff, = ax.plot([1, 2e3], [0.4, 0.4], color='darkturquoise', linestyle='--')
    ax.axhspan(0, 0.4, color='darkturquoise', alpha=0.3)
    ax.text(5e2, 0.2, f"$\\xi$ < 0.4", ha="center", va="center", fontsize=14, color = "darkturquoise")

#Colors
    #cmap = matplotlib.colormaps.get_cmap(cmap_name)
    cmap = matplotlib.colormaps.get_cmap('tab10')
    n = len(Branch_Ratio_plot)

    colors = [cmap(i) for i in range(n)]
    colors[3] = 'purple'

    legend_handles = []
    
    """Branch_Ratio = 1e-2
    Events = np.loadtxt(f"N={Branch_Ratio:.2e}.txt")
    #Events = np.ma.masked_greater(Events, 10)
    pcm = ax.pcolormesh(X, Y, Events, shading="auto", cmap="viridis")
    plt.colorbar(pcm, ax=ax, label="Number of Events")"""

    for idx, Branch_Ratio_D in enumerate(Branch_Ratio_plot):
        sigma_levels = [-2]
        fmt_dict = {-2: f"{Branch_Ratio_D:.1e}"}
        N = np.loadtxt(f"../Texts/N_BR={Branch_Ratio_D:.2e}-0.01eV-{k_res}x{w_res}-Eta={Eta_D:.2e}-{A_eff}_A_eff.csv", delimiter = " ")
        CS = ax.contour(X, Y, N, levels=sigma_levels, colors=[colors[idx]], linestyles = "-", linewidths=2)
        ax.text(xpos[idx], ypos[idx],f"BR = {sci_label_unicode(float(fmt_dict[-2]))}",  ha="center", va="center", fontsize=14, color = colors[idx], rotation = Rotations[idx])
        
    text = (f"$\\eta$ = {sci_label_unicode(Eta_D, -1)}\n$m_\\nu$ = 0.01 eV")
    ax.text(1.4e2, 4.6, text, ha="left", va="center", fontsize=14, color = "white")
    ax.set_xlim(left=10e-1 , right = 1e3)
    ax.set_ylim(bottom=0 , top=5)   
    ax.set_xlabel(r"$m_{\pi_D}$ [MeV]", size = 16)
    #ax.set_ylabel(r"$\zeta$", size = 14)
    ax.set_ylabel(r"$\xi = m_{\pi_D}/f_{\pi_D}$", size = 16)
    ax.set_xscale('log')
    plt.tick_params(direction="in",length=10,labelsize=16)
    plt.tick_params(which="minor",direction="in",length=4)
    ax.tick_params(axis='both', which='both', top=True, bottom=True, left=True, right=True)
    plt.tick_params(axis='x',pad=7)
    #plt.grid()
    pdf.savefig(bbox_inches="tight")
    plt.close()