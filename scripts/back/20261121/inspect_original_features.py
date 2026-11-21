import os
from pathlib import Path

orig = Path(r"C:\Workspaces\fundetaxcol_flutter\lib")

def show_file_snippet(rel_path, max_lines=150):
    p = orig / rel_path
    if not p.exists():
        print(f"NOT FOUND: {rel_path}")
        return
    print(f"\n=================== {rel_path} ===================")
    lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
    for i, line in enumerate(lines[:max_lines], 1):
        print(f"{i:3d}: {line}")
    if len(lines) > max_lines:
        print(f"... and {len(lines) - max_lines} more lines.")

# 1. Payment list controller & view
show_file_snippet("controllers/list/payment_list.controller.dart")
show_file_snippet("ui/views/list/pago_list_view.dart")

# 2. Turn list controller & view
show_file_snippet("controllers/list/turn_list.controller.dart")
show_file_snippet("ui/views/list/turno_list_view.dart")

# 3. Despacho list view
show_file_snippet("ui/views/list/despacho_list_view.dart")

# 4. Bahía selected controller & view
show_file_snippet("controllers/root/bahia_selected.controller.dart")
show_file_snippet("ui/views/main/bahia_selected_view.dart")

# 5. Pago form
show_file_snippet("ui/views/form/pago_form_view.dart")
show_file_snippet("controllers/models/pago.controller.dart")
