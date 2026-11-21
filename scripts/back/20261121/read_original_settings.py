import os

path = r"C:\Workspaces\fundetaxcol_flutter\lib\storage\settings.storage.dart"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        print(f.read())
else:
    print("No existe settings.storage.dart")
