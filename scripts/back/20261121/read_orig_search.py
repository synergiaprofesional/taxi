from pathlib import Path

orig = Path(r"C:\Workspaces\fundetaxcol_flutter\lib")

def show(rel):
    print(f"\n=================== {rel} ===================")
    p = orig / rel
    if p.exists():
        print(p.read_text(encoding="utf-8", errors="ignore"))

show("classes/vehiculo.dart")
show("classes/conductor.dart")
show("controllers/search/vehiculo.search.controller.dart")
show("controllers/search/search.controller.dart")
