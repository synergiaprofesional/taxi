from pathlib import Path

p = Path(r"C:\Workspaces\synergia_movil\android\app\src\main")
for f in p.rglob("*.*"):
    if f.suffix in [".xml", ".kt", ".java"]:
        print(f"\n=================== {f.name} ===================")
        print(f.read_text(encoding="utf-8", errors="ignore"))
