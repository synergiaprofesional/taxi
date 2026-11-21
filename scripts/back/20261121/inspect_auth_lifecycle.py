from pathlib import Path

def show_file_head(path, lines=100):
    print(f"\n=================== {path} ===================")
    if not path.exists():
        print("NOT FOUND")
        return
    text = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for i, l in enumerate(text[:lines], 1):
        print(f"{i:2d}: {l}")

new_p = Path(r"C:\Workspaces\synergia_movil\lib")
orig_p = Path(r"C:\Workspaces\fundetaxcol_flutter\lib")

show_file_head(new_p / "main.dart")
show_file_head(new_p / "ui/views/auth/auth_gatekeeper.dart")
show_file_head(new_p / "services/odoo_service.dart", 120)

show_file_head(orig_p / "main.dart")
show_file_head(orig_p / "ui/widgets/root/splash_widget.dart")
show_file_head(orig_p / "controllers/root/root.controller.dart")
show_file_head(orig_p / "controllers/global/auth.controller.dart")
