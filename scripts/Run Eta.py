import subprocess

Branch_Ratio_D = 1e-6
A_eff = ["Average"]
Resolution = 100

Cases = {
    "Average": 
    [1, 10, 1e3, 1e8],
}

processes = []
for Area in A_eff:
    for Overdensity_D in Cases[Area]:
        processes.append(subprocess.Popen(["python", "../Source/Eta.py", str(Overdensity_D), str(Branch_Ratio_D), str(Resolution), str(Area)]))

for p in processes:
    p.wait()