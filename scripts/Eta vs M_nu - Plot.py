from Functions import *

M_Pi_plot = [1, 5, 10, 50, 100]
Xi_plot = [0.5]

k_res = w_res = 100
Branch_Ratio_D = 4e-7
A_eff_string = "Average"

#with PdfPages(f"../PDFs/Eta vs m_nu - BR = {Branch_Ratio_D} - Zeta Comp.pdf") as pdf:
with PdfPages(f"../PDFs/Eta vs m_nu - BR = {Branch_Ratio_D} - M_pi Comp.pdf") as pdf:

    start_time = time.time()
    fig, ax = plt.subplots(figsize=(6, 6))

#Katrin
    x, y = interpolate_function('../Texts/Katrin.txt', True, 1.6639e-2, 0, 10000)
    Katrin, = ax.plot(np.sqrt(x), y, '-', color='black')
    ax.fill_between(x, y, 1e13, color='grey', alpha=1)
    ax.text(1.1e-2, 2.5e11, r"$\mathrm{KATRIN^{a}}$", color="Black", ha="center", va="center", fontsize=14, rotation = 0)                                                                                                                   

#Smirnov
    p, u = interpolate_function('../Texts/Self Interaction.txt', False, 0, 0, 10000)
    Smirnov, = ax.plot(p, 10**u, linestyle = 'dashdot', color='red')
    ax.text(1.6e-1, 4e7, "Self-Interaction", color="red", ha="center", va="center", fontsize=14, rotation=32) 

#Pierre Auger
    m, n = interpolate_function('../Texts/Pierre Auger.txt', True, 0, 0, 10000)
    Pierre_Auger, = ax.plot(m, n, linestyle = 'dotted', color='blue')
    ax.text(1.1e-2, 2e10, "Pierre Auger", color="blue", ha="center", va="center", fontsize=14, rotation=0)
    
#IceCube
    w, v = interpolate_function('../Texts/IceCube - Eta vs M_nu.txt', True, 0, 0, 10000)
    IceCube, = ax.plot(w, v, linestyle = 'dotted', color='green')
    ax.text(1.1e-2, 2e9, r"$\mathrm{IceCube^{a}}$", color="green", ha="center", va="center", fontsize=14, rotation=0)

#Pauli Blocking
    Pauli = ax.axhline(y=2e4, color='saddlebrown', linestyle = 'dashdot')
    ax.text(5.2e-3, 5e4, r"Pauli Blocking", color="saddlebrown", ha="center", va="center", fontsize=14, rotation=0)

#NH_SFR
    f, g = interpolate_function('../Texts/NH SFR.txt', True, 0, 0, 10000)
    NH_SFR, = ax.plot(f, g, linestyle = 'dotted', color='darkgoldenrod')
    ax.text(1.2e-1, 1.5e5, r"$\mathrm{IceCube^{b}}$", ha="center", va="center", fontsize=14, color = "darkgoldenrod", rotation = -20)  

#DESI+CMB
    m_nu_1 = 0.003968722834097808 #Found using Roots.py for M = m_1 + m_2 + m_3 = 0.064 eV using Normal Ordering
    DESI = ax.axvline(x=m_nu_1, color='purple', linestyle='--')
    ax.text(3.2e-3, 2.3e7, "DESI+CMB", ha="center", va="center", fontsize=14, color = "purple", rotation = 90)
    
#PLANCK+BAO
    m_nu_1 = 0.03006717647218883 #Found using Roots.py for M = m_1 + m_2 + m_3 = 0.12 eV using Normal Ordering
    Pauli = ax.axvline(x=m_nu_1, color='yellowgreen', linestyle='--')
    ax.text(2.5e-2, 3.3e7, "Planck+BAO", ha="center", va="center", fontsize=14, color = "yellowgreen", rotation = 90)
    
#Lokhov_Tkachov 
    Lokhov_Tkachov  = ax.axvline(x=0.45, color='darkturquoise', linestyle='--')
    ax.axvspan(0.45, 1, color="darkturquoise", alpha=0.2)
    ax.text(0.38, 1e6, r"$\mathrm{KATRIN^{b}}$", ha="center", va="center", fontsize=14, color = "darkturquoise", rotation = 90)

    
    X = np.loadtxt(f"../Texts/M_nu-(Eta vs M_nu)-{k_res}x{w_res}.csv", delimiter = " ")
    Y = np.loadtxt(f"../Texts/Eta-(Eta vs M_nu)-{k_res}x{w_res}.csv", delimiter = " ")

    colors = ["dimgrey", "darkcyan", "orchid", "darkorange", "navy"]

    legend_handles = []
    max_y = np.inf
    index = 0
    for idx, Xi_D in enumerate(Xi_plot):
        for idx, m_pi_D in enumerate(M_Pi_plot):
            N = np.loadtxt(f"../Texts/N_(Eta vs M_nu)-(Xi vs M_pi vs BR)={Xi_D:.2e}-{m_pi_D:.2e}-{Branch_Ratio_D:.2e}-{k_res}x{w_res}-{A_eff_string}_A_eff.csv", delimiter = " ")
            sigma_levels = [-2]
            fmt_dict = {-2: f"$m_{{\\pi_D}}$ = {m_pi_D:.0f} MeV, $\\zeta$ = {Xi_D:.2f}"}
            CS = ax.contour(X / eV, Y, N, levels=sigma_levels, linestyles='-', colors=colors[index], linewidths=2)
            label = f"$m_{{\\pi_D}}$={m_pi_D:.0f} MeV"
            #label = f"$\\zeta$={Zeta_D:.2f}"

            legend_handles.append(Line2D([0], [0], color=colors[index], linestyle="-", lw=2, label=label))
            index += 1
            print(index)
    text = (f"BR = {sci_label_unicode(Branch_Ratio_D, 0)}\n$\\xi$ = {Xi_D:.2f}")
    #text = (f"BR = {sci_label_unicode(Branch_Ratio_D)}\n$m_{{\\pi_D}}$={m_pi_D:.0f} MeV")
    
    #text = (f"$m_\\nu$ = 0.01eV")
    ax.text(0.60, 0.03, text, transform=ax.transAxes, ha="left", va="bottom", fontsize=14)
    #ax.set_xlim(left=1e-15, right = 1e-7)
    ax.set_ylim(bottom=1, top=1e13)   
    ax.set_xlim(left=1e-3, right = 1)
    ax.set_xlabel(f"$m_\\nu$ [eV]", size = 16)
    #ax.set_xlabel(r"Branching Ratio", size = 16)
    ax.set_ylabel(r"$\eta$", size=16)

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.xaxis.set_major_locator(LogLocator(base=10, subs=(1.0,), numticks=100))
    ax.xaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10), numticks=100))

    ax.yaxis.set_major_locator(LogLocator(base=10, subs=(1.0,), numticks=100))
    ax.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10), numticks=100))

    ax.xaxis.set_major_formatter(LogFormatterMathtext(base=10))
    ax.yaxis.set_major_formatter(LogFormatterMathtext(base=10))

    plt.tick_params(which="major", direction="in", length=10, labelsize=16)

    plt.tick_params(axis = "both", which="minor", direction="in", length=4)

    plt.tick_params(axis='both', which='both', top=True, bottom=True, left=True, right=True)

    plt.tick_params(axis='x', which='both', top=True, labeltop=False)
    plt.tick_params(axis='y', which='both', right=True, labelright=False)

    plt.tick_params(axis='x',pad=7)
    ax.legend(handles=legend_handles, loc="upper right", borderaxespad=0., handlelength=1.5, fontsize = 12)
    
    #plt.grid(which="major", alpha=0.5)  
    pdf.savefig(bbox_inches="tight")
    plt.close()
    
    elapsed_time = time.time() - start_time
    print("Time Elapsed:", Elapsed_Time(elapsed_time))