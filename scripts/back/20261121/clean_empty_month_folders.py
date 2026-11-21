#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/clean_empty_month_folders.py
Elimina las carpetas de meses dentro de Bitacoras/2026 que no tienen ningun archivo.
Conserva unicamente los meses con contenido real (ej: mes 10 y mes 11).
"""

import os
import shutil

WORKSPACE = r"c:\Workspaces\synergia_movil"
BITACORAS_2026 = os.path.join(WORKSPACE, "Bitacoras", "2026")

def clean_empty_months():
    print("=== Depuracion de carpetas de meses vacios en Bitacoras/2026 ===")
    
    if not os.path.exists(BITACORAS_2026):
        print("No existe Bitacoras/2026")
        return

    months = sorted(os.listdir(BITACORAS_2026))
    deleted_months = []
    kept_months = []

    for m in months:
        m_path = os.path.join(BITACORAS_2026, m)
        if not os.path.isdir(m_path):
            continue

        # Contar archivos recursivamente dentro del mes
        files = []
        for root, dirs, filenames in os.walk(m_path):
            for f in filenames:
                files.append(os.path.join(root, f))

        if len(files) == 0:
            shutil.rmtree(m_path)
            deleted_months.append(m)
            print(f"  [ELIMINADO] Mes {m}: 0 archivos")
        else:
            kept_months.append((m, len(files)))
            print(f"  [CONSERVADO] Mes {m}: {len(files)} archivo(s)")

    print(f"\n[OK] Resumen:")
    print(f"  - Meses eliminados por no tener contenido: {deleted_months}")
    print(f"  - Meses conservados con contenido: {[m for m, count in kept_months]}")

if __name__ == "__main__":
    clean_empty_months()

