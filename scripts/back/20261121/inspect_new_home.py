from pathlib import Path

new_lib = Path(r"C:\Workspaces\synergia_movil\lib")

def show(rel):
    print(f"\n=================== {rel} ===================")
    p = new_lib / rel
    if not p.exists():
        print("NOT FOUND")
        return
    print(p.read_text(encoding="utf-8", errors="ignore"))

show("ui/views/home/home_view.dart")
