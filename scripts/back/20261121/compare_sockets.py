from pathlib import Path

def show(path):
    print(f"\n=================== {path} ===================")
    if not path.exists():
        print("NOT FOUND")
        return
    print(path.read_text(encoding="utf-8", errors="ignore"))

show(Path(r"C:\Workspaces\synergia_movil\lib\services\socket_service.dart"))
show(Path(r"C:\Workspaces\fundetaxcol_flutter\lib\controllers\global\socket.controller.dart"))
