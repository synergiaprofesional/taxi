import os

ORIGINAL_DIR = r"C:\Workspaces\fundetaxcol_flutter"

for root, dirs, files in os.walk(os.path.join(ORIGINAL_DIR, "lib")):
    for f in files:
        if "pago" in f.lower() or "payment" in f.lower():
            path = os.path.join(root, f)
            rel = os.path.relpath(path, ORIGINAL_DIR)
            print("VISTA/ARCHIVO:", rel)
