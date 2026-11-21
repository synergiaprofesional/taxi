#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/clean_empty_bitacoras_days.py
Elimina las subcarpetas de días vacías dentro de Bitacoras/2026 para los meses 01 a 11.
Conserva intactas las subcarpetas de días que contienen archivos y el mes 12.
"""

import os

WORKSPACE = r"c:\Workspaces\synergia_movil"
BITACORAS_2026 = os.path.join(WORKSPACE, "Bitacoras", "2026")

TARGET_MONTHS = [f"{m:02d}" for m in range(1, 12)]  # 01 a 11

def clean_empty_day_folders():
    deleted_count = 0
    kept_count = 0

    print("=== Limpieza de subcarpetas de días vacías en Bitacoras/2026 (Meses 01 a 11) ===")

    for m in TARGET_MONTHS:
        m_path = os.path.join(BITACORAS_2026, m)
        if not os.path.exists(m_path):
            continue

        days = sorted(os.listdir(m_path))
        for d in days:
            d_path = os.path.join(m_path, d)
            if not os.path.isdir(d_path):
                continue

            items = os.listdir(d_path)
            if len(items) == 0:
                os.rmdir(d_path)
                deleted_count += 1
            else:
                kept_count += 1
                print(f"  [CONSERVADA] Mes {m}, Día {d}: {len(items)} archivo(s)")

    print(f"\n[OK] Resumen:")
    print(f"  - Subcarpetas de días vacías eliminadas: {deleted_count}")
    print(f"  - Subcarpetas de días con archivos conservadas: {kept_count}")

if __name__ == "__main__":
    clean_empty_day_folders()

