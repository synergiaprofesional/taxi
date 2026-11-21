#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: scripts/run_flutter_test.py
Descripción: Ejecutor de tests unitarios y de widgets para Synergia Móvil
Ubicación obligatoria: scripts/ (Regla Inviolable #1)
"""

import subprocess
import sys

print("[TEST] Ejecutando flutter test...", flush=True)
res = subprocess.run("cmd.exe /c flutter test --no-pub", shell=True, capture_output=True, text=True)
print(res.stdout, flush=True)
if res.stderr:
    print(res.stderr, file=sys.stderr, flush=True)
sys.exit(res.returncode)

