from Functions import *
#================================================================================= initialization ====================================================================
with PdfPages("../PDFs/Spectrum.pdf") as pdf:
#=========================================================================== plot Flux vs Neutrino Energy ==========================================================================
    start_time = time.time()
    #plot Flux vs Neutrino Energy
    plt.figure(figsize=(6, 6))

    x , y = interpolate_function('../Texts/Events.txt', True, 0, 0, 100)
    plt.plot(x, y, color="red", label = "Events", linewidth=2)
    
    plt.xscale('log')
    plt.xlabel('Neutrino Energy [GeV]', size = 16)
    plt.ylabel('Number of Events', size = 16)
    plt.xlim(left = 1e8, right = 1e11)
    plt.legend(loc="center right", borderaxespad=0., handlelength=1.5, fontsize = 12)
    plt.tick_params(direction="in",length=10,labelsize=16)
    plt.tick_params(which="minor",direction="in",length=4)
    plt.tick_params(axis='both', which='both', top=True, bottom=True, left=True, right=True)
    plt.tick_params(axis='x',pad=7)
    pdf.savefig(bbox_inches="tight")
    plt.close()

    elapsed_time = time.time() - start_time
    print("Time Elapsed:", Elapsed_Time(elapsed_time))