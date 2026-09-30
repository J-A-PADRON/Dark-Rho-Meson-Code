from Functions import *
#================================================================================= initialization ====================================================================
with PdfPages("../PDFs/Effective Areas.pdf") as pdf:
#=========================================================================== plot Flux vs Neutrino Energy ==========================================================================
    start_time = time.time()

    plt.figure(figsize=(6, 6))

    Old_Energy, Old_A_eff_Array = np.loadtxt('../Texts/Gen2_effective_areas.txt', delimiter = ",", unpack = True)

    Old_Energy = 10**Old_Energy * (eV / GeV)
    Old_A_eff_Array = Old_A_eff_Array
    plt.plot(Old_Energy, Old_A_eff_Array/Old_Energy, color="purple", label = r"Old", linewidth=2)
    plt.plot(Electron_Energy, Electron_A_eff_Array/Electron_Energy, color="red", label = r"e", linewidth=2)
    plt.plot(Muon_Energy, Muon_A_eff_Array/Muon_Energy, color="green", label = r"$\mu$", linewidth=2)
    plt.plot(Tau_Energy, Tau_A_eff_Array/Tau_Energy, color="blue", label = r"$\tau$", linewidth=2)
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Energy [GeV]', size = 16)
    plt.ylabel(f'Effective Area $[m^{2}]$ / Energy [GeV]', size = 16)
    plt.xlim(left = 1e7, right = 1e11)
    #plt.ylim(bottom = 1, top = 1e7)
    plt.legend(loc="center right", borderaxespad=0., handlelength=1.5, fontsize = 12)
    plt.tick_params(direction="in",length=10,labelsize=16)
    plt.tick_params(which="minor",direction="in",length=4)
    plt.tick_params(axis='both', which='both', top=True, bottom=True, left=True, right=True)
    plt.tick_params(axis='x',pad=7)
    pdf.savefig(bbox_inches="tight")
    plt.close()

    elapsed_time = time.time() - start_time
    print("Time Elapsed:", Elapsed_Time(elapsed_time))