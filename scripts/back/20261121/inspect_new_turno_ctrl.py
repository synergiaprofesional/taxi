from pathlib import Path

new_lib = Path(r"C:\Workspaces\synergia_movil\lib")

def show_code(rel):
    print(f"\n=================== {rel} ===================")
    p = new_lib / rel
    if not p.exists():
        print("NOT FOUND")
        return
    print(p.read_text(encoding="utf-8", errors="ignore"))

show_code("controllers/turno_controller.dart")
