import os

ORIGINAL_DIR = r"C:\Workspaces\fundetaxcol_flutter"

target_files = [
    r"lib\controllers\models\pago.controller.dart",
    r"lib\storage\payment.storage.dart",
    r"lib\controllers\global\preferences.controller.dart"
]

for rel in target_files:
    full_path = os.path.join(ORIGINAL_DIR, rel)
    print(f"\n========================================================")
    print(f"ARCHIVO: {rel}")
    print(f"========================================================")
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
            lines = fp.readlines()
            for idx, line in enumerate(lines[:120]):
                print(f"{idx+1:3d}: {line}", end="")
            if len(lines) > 120:
                print(f"\n... [Total lineas: {len(lines)}]")
    else:
        print("No existe.")
