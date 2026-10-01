import subprocess

Overdensities = [1, 1e11]
A_eff = ["Average"]
Resolution = 100

Branch_Ratios = {
    (1, "Average"): 
    [4.7e-7, 1e-6, 4e-6, 1e-4],
    
    (1e11, "Average"): 
    [5.2e-14, 1.2e-13, 1e-12, 1e-8]
}

processes = []
for Eta_D in Overdensities:
    for Area in A_eff:
        for Branch_Ratio_D in Branch_Ratios[Eta_D, Area]:
            processes.append(subprocess.Popen(["python", "../Source/BR.py", str(Eta_D), str(Branch_Ratio_D), str(Resolution), str(Area)]))

for p in processes:
    p.wait()