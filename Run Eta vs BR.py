from Functions import *
import subprocess

A_eff = ["Average", "Electron"]
Resolution = 100
#M_Pi_plot = np.logspace(-2, 2, 25)
Xi_plot = [0.5, 1]
M_Pi_plot = [5, 10, 50, 100]

processes = []

for Area in A_eff:
    for m_pi_D in M_Pi_plot:
        for Xi_D in Xi_plot:
            processes.append(subprocess.Popen(["python", "Eta vs BR.py", str(Area), str(Resolution), str(m_pi_D), str(Xi_D)]))
            if len(processes) == 20:
                for p in processes:
                    p.wait()
                processes = []
            
for p in processes:
    p.wait()