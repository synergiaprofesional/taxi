import os

path = r"C:\Workspaces\fundetaxcol_flutter\lib\classes\pago.dart"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        print(f.read())
