from pathlib import Path

p = Path(r"C:\Workspaces\synergia_movil\lib\ui\views\auth\login_view.dart")
lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
for i, line in enumerate(lines[149:300], 150):
    print(f"{i:3d}: {line}")
