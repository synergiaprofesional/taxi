#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/organize_bitacoras.py
Organización jerárquica obligatoria de Bitacoras en YYYY/MM/DD.
Estructura carpetas para el año 2026 (meses 01..12 y días 01..28/30/31).
Mueve los archivos existentes a sus carpetas correspondientes y actualiza bitacoras.md.
"""

import os
import re
import shutil
import calendar

WORKSPACE = r"c:\Workspaces\synergia_movil"
BITACORAS_DIR = os.path.join(WORKSPACE, "Bitacoras")

DAYS_IN_MONTH_2026 = {
    1: 31,
    2: 28,  # 2026 no es bisiesto
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}

def create_year_structure(year=2026):
    print(f"=== Creando estructura jerárquica para el año {year} ===")
    created_count = 0
    for month in range(1, 13):
        m_str = f"{month:02d}"
        days = DAYS_IN_MONTH_2026[month]
        for day in range(1, days + 1):
            d_str = f"{day:02d}"
            folder_path = os.path.join(BITACORAS_DIR, str(year), m_str, d_str)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
                created_count += 1
    print(f"[OK] Creadas {created_count} carpetas de días para el año {year}.")

def organize_files():
    print("\n=== Reorganizando archivos existentes de Bitácoras ===")
    moved_count = 0
    file_mapping = {}  # old_rel_path -> new_rel_path

    # Regex patterns
    # 1. Bitacora ddmmaaaa.md (ej: Bitacora 07112026.md)
    re_daily = re.compile(r"^Bitacora\s+(\d{2})(\d{2})(\d{4})\.md$", re.IGNORECASE)
    # 2. Bitacora YYYYMMDD HHmmss.md (ej: Bitacora 20261107 133500.md)
    re_atomic = re.compile(r"^Bitacora\s+(\d{4})(\d{2})(\d{2})\s+(\d{6})\.md$", re.IGNORECASE)

    for item in os.listdir(BITACORAS_DIR):
        item_path = os.path.join(BITACORAS_DIR, item)
        if not os.path.isfile(item_path):
            continue
        
        if item.lower() in ["bitacoras.md", ".env", "readme.md"]:
            continue

        match_daily = re_daily.match(item)
        match_atomic = re_atomic.match(item)

        target_dir = None
        if match_daily:
            day, month, year = match_daily.groups()
            target_dir = os.path.join(BITACORAS_DIR, year, month, day)
        elif match_atomic:
            year, month, day, _ = match_atomic.groups()
            target_dir = os.path.join(BITACORAS_DIR, year, month, day)

        if target_dir:
            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, item)
            shutil.move(item_path, target_path)
            old_rel = f"Bitacoras/{item}"
            new_rel = f"Bitacoras/{year}/{month}/{day}/{item}"
            file_mapping[item] = f"{year}/{month}/{day}/{item}"
            moved_count += 1
            print(f"  -> Movido: {item} => {year}/{month}/{day}/")

    print(f"[OK] Total de archivos movidos: {moved_count}")
    return file_mapping

def update_bitacoras_index(file_mapping):
    index_path = os.path.join(BITACORAS_DIR, "bitacoras.md")
    if not os.path.exists(index_path):
        return

    print("\n=== Actualizando enlaces en bitacoras.md ===")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Reemplazar rutas en enlaces markdown o file:///
    # Ejemplos comunes:
    # [Bitacora Diaria...](file:///.../Bitacoras/Bitacora%2007112026.md)
    # [Bitacora Sesión...](file:///.../Bitacoras/Bitacora%2020261107%20133500.md)
    # Bitacoras/Bitacora 07112026.md
    for old_filename, new_rel in file_mapping.items():
        # old_filename: "Bitacora 07112026.md"
        # new_rel: "2026/11/07/Bitacora 07112026.md"
        encoded_old = old_filename.replace(" ", "%20")
        encoded_new = new_rel.replace(" ", "%20")

        # Patrones con Bitacoras/ y sin Bitacoras/
        content = content.replace(f"Bitacoras/{old_filename}", f"Bitacoras/{new_rel}")
        content = content.replace(f"Bitacoras/{encoded_old}", f"Bitacoras/{encoded_new}")
        content = content.replace(f"Bitacoras\\{old_filename}", f"Bitacoras/{new_rel}")
        content = content.replace(f"/{encoded_old}", f"/{encoded_new}")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("[OK] bitacoras.md actualizado exitosamente con las nuevas rutas.")

if __name__ == "__main__":
    create_year_structure(2026)
    mapping = organize_files()
    update_bitacoras_index(mapping)
    print("\n=== Reorganización completada con éxito ===")

