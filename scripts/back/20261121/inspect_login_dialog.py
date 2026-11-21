from pathlib import Path

def show(path):
    print(f"\n=================== {path} ===================")
    if not path.exists():
        print("NOT FOUND")
        return
    print(path.read_text(encoding="utf-8", errors="ignore"))

show(Path(r"C:\Workspaces\synergia_movil\lib\ui\views\auth\login_dialog.dart"))
