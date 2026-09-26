"""NHANES scouting part 2: 2015-2016 cycle (I) - the cycle WITH screen-time items."""
import urllib.request, os
import pandas as pd

BASE = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2015/DataFiles/"
OUT = r"C:\Users\masum\Desktop\Vrunda\sleep project\data\raw\nhanes\\"
FILES = ["DEMO_I.xpt", "SLQ_I.xpt", "PAQ_I.xpt"]
H = {"User-Agent": "Mozilla/5.0"}

for f in FILES:
    path = OUT + f
    try:
        if not os.path.exists(path):
            data = urllib.request.urlopen(urllib.request.Request(BASE + f, headers=H), timeout=120).read()
            open(path, "wb").write(data)
            print(f, "downloaded", len(data), "bytes")
        df = pd.read_sas(path, format="xport")
        print(" ", f, "shape:", df.shape)
        print("  cols:", list(df.columns))
    except Exception as e:
        print(f, "FAIL", repr(e)[:120])
