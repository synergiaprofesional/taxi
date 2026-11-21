import os
import re

ORIGINAL_DIR = r"C:\Workspaces\fundetaxcol_flutter"

print("=== BUSCANDO CONSULTAS DE PAGO EN fundetaxcol_flutter ===")

keywords = ["fundetaxcol.pago", "cargarPagos", "getPagos", "pago_service", "payment_service", "pago_controller", "pago_dao"]

matches = []

for root, dirs, files in os.walk(ORIGINAL_DIR):
    for f in files:
        if f.endswith(".dart"):
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()
                    for kw in keywords:
                        if kw in content:
                            matches.append((path, kw))
                            break
            except Exception as e:
                pass

print(f"Archivos encontrados con referencias a pagos: {len(matches)}")
for path, kw in matches:
    rel = os.path.relpath(path, ORIGINAL_DIR)
    print(f" - {rel} (coincidencia: {kw})")
