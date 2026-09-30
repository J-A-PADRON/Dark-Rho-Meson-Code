import subprocess

Overdensities = [1]

Branch_Ratios = {
    (1, "Electron"): [2.7e-7, 7e-7, 1e-5, 1e-2],
    (1, "Average"): [4.7e-7, 1e-6, 4e-6, 1e-4],
    (1e11, "Electron"): [3.3e-14, 8e-14, 1e-12, 1e-8],
    (1e11, "Average"): [2.4e-13]
}

A_eff = ["Average"]

Resolution = 300
stepsize = 1.05

processes = []

for Eta_D in Overdensities:
    for Area in A_eff:
        for Branch_Ratio_D in Branch_Ratios[Eta_D, Area]:
            processes.append(subprocess.Popen(["python", "BR.py", str(Eta_D), str(Branch_Ratio_D), str(Resolution), str(Area), str(stepsize)]))

for p in processes:
    p.wait()