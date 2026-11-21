from pathlib import Path

p = Path(r"C:\Workspaces\synergia_movil\lib\models\vehicle_model.dart")
print(p.read_text(encoding="utf-8", errors="ignore"))
