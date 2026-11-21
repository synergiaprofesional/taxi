from pathlib import Path

orig = Path(r"C:\Workspaces\fundetaxcol_flutter\lib")

def show_head(rel, n=80):
    print(f"\n=================== {rel} ===================")
    p = orig / rel
    lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
    for i, line in enumerate(lines[:n], 1):
        print(f"{i:2d}: {line}")

show_head("controllers/list/payment_list.controller.dart", 80)
show_head("controllers/list/turn_list.controller.dart", 80)
