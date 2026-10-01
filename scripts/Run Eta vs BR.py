import subprocess

A_eff = ["Average"]
Resolution = 100
Xi_plot = [0.5]
M_Pi_plot = [1, 5, 10, 50, 100]

processes = []
for Area in A_eff:
    for m_pi_D in M_Pi_plot:
        for Xi_D in Xi_plot:
            processes.append(subprocess.Popen(["python", "../Source/Eta vs BR.py", str(Area), str(Resolution), str(m_pi_D), str(Xi_D)]))
            if len(processes) == 20:
                for p in processes:
                    p.wait()
                processes = []
            
for p in processes:
    p.wait()