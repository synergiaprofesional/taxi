from pathlib import Path

orig = Path(r"C:\Workspaces\fundetaxcol_flutter\lib")

def show(rel):
    print(f"\n=================== {rel} ===================")
    p = orig / rel
    print(p.read_text(encoding="utf-8", errors="ignore"))

show("controllers/list/payment_list.controller.dart")
show("controllers/list/turn_list.controller.dart")
show("ui/views/list/despacho_list_view.dart")
show("storage/payment.storage.dart")
show("storage/turn.storage.dart")
