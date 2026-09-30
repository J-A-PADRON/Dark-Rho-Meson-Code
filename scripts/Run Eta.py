import subprocess

Branch_Ratio_D = 1e-6

Cases = {
    "Average": [10, 20, 30, 40],
    #"Electron": [8.5, 30, 1e3, 1e9]
}

A_eff = ["Average"]

Resolution = 100

processes = []

for Area in A_eff:
    for Overdensity_D in Cases[Area]:
        processes.append(subprocess.Popen(["python", "Eta.py", str(Overdensity_D), str(Branch_Ratio_D), str(Resolution), str(Area)]))

for p in processes:
    p.wait()