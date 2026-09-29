import subprocess

M_Pi_plot = [1, 5, 10, 50, 100]

Xi_plot = [0.5]

Branch_Ratios = [2e-7, 3e-7, 4e-7, 5e-7]

A_eff = ["Average"]

Resolution = 100

processes = []

for Branch_Ratio_D in Branch_Ratios:
    for Xi_D in Xi_plot:
        for Area in A_eff:
            for m_pi_D in M_Pi_plot:

                processes.append(subprocess.Popen(["python", "Eta vs M_nu.py", str(m_pi_D), str(Xi_D), str(Branch_Ratio_D), str(Area), str(Resolution)]))

                if len(processes) == 20:
                    for p in processes:
                        p.wait()
                    processes = []

for p in processes:
    p.wait()