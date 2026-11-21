from pathlib import Path

p = Path(r"C:\Workspaces\synergia_movil\lib\services\odoo_service.dart")
lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
for i, line in enumerate(lines[:100], 1):
    print(f"{i:3d}: {line}")
