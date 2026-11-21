from pathlib import Path

def show(rel):
    print(f"\n=================== {rel} ===================")
    p = Path(r"c:\Workspaces\synergia_movil\openspec\specs") / rel / "spec.md"
    if p.exists():
        print(p.read_text(encoding="utf-8", errors="ignore"))

show("view-pago-list")
show("view-despacho-list")
show("view-bahia-selected-shell")
