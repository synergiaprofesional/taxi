from pathlib import Path

orig = Path(r"C:\Workspaces\fundetaxcol_flutter\lib\storage\storage.dart")
print(orig.read_text(encoding="utf-8", errors="ignore"))
