from pathlib import Path

orig = Path(r"C:\Workspaces\fundetaxcol_flutter\lib")

def show_file(rel_path):
    p = orig / rel_path
    if not p.exists():
        print(f"NOT FOUND: {rel_path}")
        return
    print(f"\n=================== {rel_path} ===================")
    content = p.read_text(encoding="utf-8", errors="ignore")
    print(content)

show_file("controllers/list/payment_list.controller.dart")
show_file("controllers/list/turn_list.controller.dart")
show_file("ui/views/list/despacho_list_view.dart")
show_file("controllers/root/bahia_selected.controller.dart")
show_file("ui/views/main/bahia_selected_view.dart")
