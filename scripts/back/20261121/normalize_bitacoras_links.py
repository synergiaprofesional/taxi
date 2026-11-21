#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/normalize_bitacoras_links.py
Normaliza todos los enlaces en Bitacoras/bitacoras.md para que apunten
limpiamente con forward slashes a file:///c:/Workspaces/synergia_movil/Bitacoras/YYYY/MM/DD/...
sin duplicaciones y sin barras invertidas.
"""

import os
import re

INDEX_PATH = r"c:\Workspaces\synergia_movil\Bitacoras\bitacoras.md"

def normalize_links():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Función de reemplazo para URLs de bitácoras
    def fix_url(match):
        label = match.group(1)
        url = match.group(2)

        # Si no es un enlace de Bitácora, no tocar
        if "Bitacora" not in url:
            return match.group(0)

        # Normalizar barras a /
        clean_url = url.replace("\\", "/")

        # Extraer el nombre del archivo (ej: Bitacora%2007112026.md o Bitacora 07112026.md)
        filename_match = re.search(r"(Bitacora(?:%20|\s+)[^/)]+\.md)", clean_url, re.IGNORECASE)
        if not filename_match:
            return match.group(0)

        raw_filename = filename_match.group(1).replace("%20", " ")

        # Determinar YYYY/MM/DD
        # Caso 1: Bitacora ddmmaaaa.md (ej: Bitacora 07112026.md)
        m_daily = re.match(r"^Bitacora\s+(\d{2})(\d{2})(\d{4})\.md$", raw_filename, re.IGNORECASE)
        # Caso 2: Bitacora YYYYMMDD HHmmss.md (ej: Bitacora 20261107 133500.md)
        m_atomic = re.match(r"^Bitacora\s+(\d{4})(\d{2})(\d{2})\s+(\d{6})\.md$", raw_filename, re.IGNORECASE)

        if m_daily:
            day, month, year = m_daily.groups()
        elif m_atomic:
            year, month, day, _ = m_atomic.groups()
        else:
            return match.group(0)

        encoded_filename = raw_filename.replace(" ", "%20")
        new_url = f"file:///c:/Workspaces/synergia_movil/Bitacoras/{year}/{month}/{day}/{encoded_filename}"
        return f"[{label}]({new_url})"

    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    new_content = pattern.sub(fix_url, content)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("[OK] Todos los enlaces de bitacoras.md fueron normalizados correctamente.")

if __name__ == "__main__":
    normalize_links()

