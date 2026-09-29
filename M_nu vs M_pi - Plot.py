from Functions import *

Xi_D = 1e9
Branch_Ratio_D = 1e-12
k_res = w_res = 100
Z_plot = [1]

Y_Offset = [-0.0005, 3e10, -1.8e-26, -8e-26, -4e-26, -1.8e-26, -8e-26, -4e-26, -1.8e-26, -8e-26]
X_Offset = [1e-1, -1.8e-26, -8e-26, -4e-26, -1.8e-26, -8e-26, -4e-26, -1.8e-26, -8e-26]
Rotations = [25]
colors = ["darkorange", "green", "teal", "red", "blue", "black", "saddlebrown", "darkviolet"] 
Positions = [15, 20, 30, 40, 46, 0, 15, 5, 0, 7, 8, 9, 10, 5, 5, 5, 5, 5, 5]



with PdfPages(f"../PDFs/M_nu vs M_pi - Zoom.pdf") as pdf:
    
    start_time = time.time()
    fig, ax = plt.subplots(figsize=(6, 6))

    Y = np.loadtxt(f"../Texts/M_nu-(M_nu vs M_pi)-{k_res}x{w_res}.csv", delimiter = " ")
    X = np.loadtxt(f"../Texts/M_pi-(M_nu vs M_pi)-{k_res}x{w_res}.csv", delimiter = " ")

    legend_handles = []
    index = 0
    for idx, Zeta_D in enumerate(Z_plot):

        N = np.loadtxt(f"../Texts/N_(M_nu vs M_pi)-(Zeta vs Eta vs BR)={Zeta_D:.2e}-{Xi_D:.2e}-{Branch_Ratio_D:.2e}-0.01eV-{k_res}x{w_res}-Eta={Xi_D:.2e}-New.csv", delimiter = " ")
        sigma_levels = [-2, 1e6, 1e7, 1.3e7, 1.5e7, 1.7e7, 1.9e7, 
                        2e7, 1e8, 2.5e8, 1e9, 1e10, 1e11, 1e12]
        fmt_dict = {-2: "-2", 1e6:"1e6", 1e7:"1e7", 1.1e7:"1e7", 1.2e7: "2e7", 1.3e7: "3e7", 1.4e7: "4e7", 1.5e7: 
                    "5e7", 1.6e7: "6e7", 1.7e7: "7e7", 
                    1.8e7: "8e7", 1.9e7: "9e7", 2e7: "2e7", 3e7: "3e7", 4e7: "4e7", 5e7: "5e7", 6e7: "6e7", 7e7: "7e7", 
                    8e7: "8e7", 9e7: "9e7", 1e8:"1e8", 2.5e8:"2.5e8", 1e9:"1e9", 1e10:"1e10", 1e11:"1e11", 1e12:"1e12"}
        CS = ax.contour(X, Y / eV, N, levels=sigma_levels, linestyles='-', colors="red", linewidths=1)
        #label_contours_offset(ax, CS, fmt_dict[-2], Positions[index], Y_Offset[0], X_Offset[0], 
                                   #fontsize = 10, rotation=Rotations[0])
        """for level in sigma_levels:
            if level in fmt_dict:
                CS_level = ax.contour(X, Y, E_res_D, levels=[level], colors=colors[index], linewidths=1)
                label_contours_offset(
                    ax,
                    CS_level,
                    fmt_dict[level],
                    idx=0,
                    y_offset=0,
                    x_offset=0,
                    fontsize=10,
                    rotation=0
                )"""
        #label = f"$m_{{\\pi_D}}$={m_pi_D:.0f} MeV"
        #label = f"$\\zeta$={Zeta_D:.2f}"

        #legend_handles.append(Line2D([0], [0], color=colors[index], lw=1, label=label))
        index += 1
        print(index)
    print("Done with Zeta = ", Zeta_D)

    text = (f"BR = {sci_label_unicode(Branch_Ratio_D)}\n$\\eta$ = {sci_label_unicode(Xi_D)}\n$\\zeta$={Zeta_D:.2f}")
    #text = (f"BR = {sci_label_unicode(Branch_Ratio_D)}\n$m_{{\\pi_D}}$={m_pi_D:.0f} MeV")
    
    #text = (f"$m_\\nu$ = 0.01eV")
    ax.text(0.03, 0.97, text, transform=ax.transAxes, ha="left", va="top", fontsize=14)

    ax.set_ylim(bottom=1e-3, top = 1)
    ax.set_xlim(left=1e-1, right = 5e2)
    #ax.set_ylim(bottom=1e-1, top=1e13)   
    ax.set_xlabel(r"$m_{\pi_D}$ [MeV]", size = 16)
    #ax.set_xlabel(r"Branching Ratio", size = 16)
    ax.set_ylabel(r"Neutrino Mass [eV]", size = 16)

    ax.set_xscale('log')
    ax.set_yscale("log")

    plt.tick_params(which="major", direction="in", length=10, labelsize=16)
    plt.tick_params(which="minor", direction="in", length=4)    
    plt.tick_params(axis='both', which='both', top=True, bottom=True, left=True, right=True)
    #ax.legend(handles=legend_handles, loc="lower right", borderaxespad=0., handlelength=1, fontsize = 10)
    #ax.legend(handles=legend_handles, loc="upper right", borderaxespad=0., handlelength=1, fontsize = 10)
    plt.tick_params(axis='x',pad=7)
    #plt.grid(which="major", alpha=0.5)  
    pdf.savefig(bbox_inches="tight")
    plt.close()
    
    elapsed_time = time.time() - start_time
    print("Time Elapsed:", Elapsed_Time(elapsed_time))