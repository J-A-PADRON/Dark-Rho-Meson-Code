import sys
sys.path.append("../Source")
from Functions import *

Xi_plot = [0.5]
A_eff = "Average"

Cases = {
    (0.5, "Average"): (
        [1, 5, 10, 50, 100],                        #m_pi
        [1.5e-7, 4.5e-8, 9e-9, 8e-7, 6e-6],          #BR
        [4e2, 4e2, 4e2, 4e2, 4e2],                  #Eta
        [-55, -55, -55, -57, -57]                   #Rotations
    )
}

M_Pi_plot, xpos, ypos, Rotations = Cases[(Xi_plot[0], A_eff)]
k_res = w_res = 100

with PdfPages(f"../Figures/Fig3_Eta_vs_BR.pdf") as pdf:    
    start_time = time.time()
    fig, ax = plt.subplots(figsize=(6, 6))

#Surinov
    Surinov = ax.axhline(y=1e7, color='red', linestyle='dashdot')
    ax.text(5e-7, 2.5e7, "Self-Interaction", ha = "center", va = "center", fontsize = 14, color = "red")

#Auger
    Auger = ax.axhline(y=8467331756.040045, color='blue', linestyle='dotted')
    ax.text(2e-9, 2e10, "Pierre Auger", ha = "center", va = "center", fontsize = 14, color = "blue")

#IceCube
    Surinov = ax.axhline(y=823410254.6982743, color='green', linestyle='dotted')
    ax.text(5e-9, 2e9, r"$\mathrm{IceCube^{a}}$", ha = "center", va = "center", fontsize = 14, color = "green")

#Pauli Blocking
    Gravity = ax.axhline(y=2e4, color='saddlebrown', linestyle='dashdot')
    ax.text(1e-11, 4e4, "Pauli Blocking", ha = "center", va = "center", fontsize = 14, color = "saddlebrown")
    
#SM Value
    SM_Value = ax.axvline(x=8e-14, color='purple', linestyle='--')
    ax.text(3e-14, 1.5e2, r"$\mathrm{BR}(\rho_{\mathrm{SM}}\to\nu_{\alpha}\bar\nu_{\alpha})$", 
            ha = "center", va = "center", fontsize = 14, color = "purple", rotation = 90)

#NH_SFR
    NH_SFR = ax.axhline(y=4.1017e+5, color='darkgoldenrod', linestyle='dotted')
    ax.text(1e-6, 9e5, r"$\mathrm{IceCube^{b}}$", ha = "center", va = "center", fontsize = 14, color = "darkgoldenrod")  
    
#Katrin Bound
    Katrin_Bound = ax.axhline(y=1.123e+11, color='black', linestyle='-')
    ax.axhspan(1.123e+11, 1e15, color='grey', alpha=1)
    ax.text(2e-10, 2.5e11, "KATRIN", ha = "center", va = "center", fontsize = 14, color = "black")

    X = np.loadtxt(f"../Results/BR-(Eta_vs_BR)-{k_res}x{w_res}.csv", delimiter = " ")
    Y = np.loadtxt(f"../Results/Eta-(Eta_vs_BR)-{k_res}x{w_res}.csv", delimiter = " ")

    colors = ["dimgrey", "darkcyan", "orchid", "darkorange", "navy"] 
    
    for idx, Xi_D in enumerate(Xi_plot):
        for idx, m_pi_D in enumerate(M_Pi_plot):
            N = np.loadtxt(f"../Results/N_(Eta_vs_BR)_Contours-Xi={Xi_D:.2e}-M_pi={m_pi_D:.2e}-{k_res}x{w_res}.csv", delimiter = " ")
            sigma_levels = [-2]
            fmt_dict = {-2: f"$m_{{\\pi_D}}$ = {m_pi_D:.0f} MeV"}
            CS = ax.contour(X, Y, N, levels=sigma_levels, linestyles='-', colors=colors[idx%5], linewidths=2)
            ax.text(xpos[idx], ypos[idx], fmt_dict[-2], ha="center", va="center",
                    fontsize=12, rotation = Rotations[idx], color = colors[idx%5])
            
    text = (f"$m_\\nu$ = 0.01 eV\n$\\xi$ = {Xi_D:.2f}")
    ax.text( 0.68, 0.96, text, transform=ax.transAxes, ha="left", va="top", fontsize=14, color = "white")
    ax.set_xlim(left=1e-15, right = 1e-4)
    ax.set_ylim(bottom=1, top=1e13)   
    ax.set_xlabel(r"$\mathrm{BR}(\rho_{\mathrm{D}}\to\nu\bar\nu)$", size = 16)
    ax.set_ylabel(r"$\eta$", size=16)
    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.xaxis.set_major_locator(LogLocator(base=10, subs=(1.0,), numticks=100))
    ax.xaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10), numticks=100))
    ax.yaxis.set_major_locator(LogLocator(base=10, subs=(1.0,), numticks=100))
    ax.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10), numticks=100))
    ax.xaxis.set_major_formatter(LogFormatterMathtext(base=10))

    for i, label in enumerate(ax.xaxis.get_ticklabels()):
        if i % 2 == 0:
            label.set_visible(False)

    plt.tick_params(which="major", direction="in", length=10, labelsize=16)
    plt.tick_params(axis = "both", which="minor", direction="in", length=4)
    plt.tick_params(axis='both', which='both', top=True, bottom=True, left=True, right=True)
    plt.tick_params(axis='x', which='both', top=True, labeltop=False)
    plt.tick_params(axis='y', which='both', right=True, labelright=False)
    plt.tick_params(axis='x',pad=7)
    pdf.savefig(bbox_inches="tight")
    plt.close()   
    elapsed_time = time.time() - start_time
    print("Time Elapsed:", Elapsed_Time(elapsed_time))