from pathlib import Path
import re

p = Path(r"C:\Workspaces\synergia_movil\lib")
patterns = ["exit(", "SystemNavigator", "closeSession", "cerrarSesion", "timeout", "Timer"]

for f in p.rglob("*.dart"):
    content = f.read_text(encoding="utf-8", errors="ignore")
    for pat in patterns:
        if pat.lower() in content.lower():
            for line_no, line in enumerate(content.splitlines(), 1):
                if pat.lower() in line.lower():
                    print(f"{f.name}:{line_no} [{pat}] -> {line.strip()}")
