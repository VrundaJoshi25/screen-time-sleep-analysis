"""NHANES scouting (guide Step 25-26): download 2017-2018 cycle files,
verify the sleep + screen-time variables exist, build the variable dictionary."""
import urllib.request, os
import pandas as pd

BASE = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/"
OUT = r"C:\Users\masum\Desktop\Vrunda\sleep project\data\raw\nhanes\\"
FILES = ["DEMO_J.xpt", "SLQ_J.xpt", "PAQ_J.xpt"]
H = {"User-Agent": "Mozilla/5.0"}

frames = {}
for f in FILES:
    path = OUT + f
    if not os.path.exists(path):
        data = urllib.request.urlopen(urllib.request.Request(BASE + f, headers=H), timeout=120).read()
        open(path, "wb").write(data)
        print(f, "downloaded", len(data), "bytes")
    else:
        print(f, "already present")
    df = pd.read_sas(path, format="xport")
    frames[f] = df
    print(" ", f, "shape:", df.shape)

print()
for f, df in frames.items():
    print("=" * 20, f, "=" * 20)
    print(list(df.columns))
