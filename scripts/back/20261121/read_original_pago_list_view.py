import os

ORIGINAL_DIR = r"C:\Workspaces\fundetaxcol_flutter"

target_files = [
    r"lib\controllers\list\payment_list.controller.dart",
    r"lib\ui\views\list\pago_list_view.dart"
]

for rel in target_files:
    path = os.path.join(ORIGINAL_DIR, rel)
    print(f"\n========================================================")
    print(f"ARCHIVO: {rel}")
    print(f"========================================================")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            print(f.read())
