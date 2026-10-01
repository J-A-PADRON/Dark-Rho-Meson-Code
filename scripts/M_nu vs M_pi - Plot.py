import sys
sys.path.append("../Source")
from Functions import *

Eta_D = 1e9
Branch_Ratio_D = 1e-12
k_res = w_res = 100
Xi_plot = [1]

with PdfPages(f"../Figures/M_nu_vs_M_pi.pdf") as pdf:
    
    start_time = time.time()
    fig, ax = plt.subplots(figsize=(6, 6))

    Y = np.loadtxt(f"../Results/M_nu-(M_nu vs M_pi)-{k_res}x{w_res}.csv", delimiter = " ")
    X = np.loadtxt(f"../Results/M_pi-(M_nu vs M_pi)-{k_res}x{w_res}.csv", delimiter = " ")

    legend_handles = []
    index = 0
    for idx, Xi_D in enumerate(Xi_plot):

        N = np.loadtxt(f"../Results/N_(M_nu_vs_M_pi)_Contours-Xi={Xi_D:.2e}-Eta={Eta_D:.2e}-BR={Branch_Ratio_D:.2e}.csv", delimiter = " ")
        sigma_levels = [-2]
        fmt_dict = {-2: "-2"}
        CS = ax.contour(X, Y / eV, N, levels=sigma_levels, linestyles='-', colors="red", linewidths=1)
        index += 1
        print(index)

    text = (f"BR = {sci_label_unicode(Branch_Ratio_D)}\n$\\eta$ = {sci_label_unicode(Eta_D)}\n$\\xi$={Xi_D:.2f}")
    ax.text(0.03, 0.97, text, transform=ax.transAxes, ha="left", va="top", fontsize=14)

    ax.set_ylim(bottom=1e-3, top = 1)
    ax.set_xlim(left=1e-1, right = 5e2)   
    ax.set_xlabel(r"$m_{\pi_D}$ [MeV]", size = 16)
    ax.set_ylabel(r"Neutrino Mass [eV]", size = 16)
    ax.set_xscale('log')
    ax.set_yscale("log")

    plt.tick_params(which="major", direction="in", length=10, labelsize=16)
    plt.tick_params(which="minor", direction="in", length=4)    
    plt.tick_params(axis='both', which='both', top=True, bottom=True, left=True, right=True)
    plt.tick_params(axis='x',pad=7)  
    pdf.savefig(bbox_inches="tight")
    plt.close()
    elapsed_time = time.time() - start_time
    print("Time Elapsed:", Elapsed_Time(elapsed_time))