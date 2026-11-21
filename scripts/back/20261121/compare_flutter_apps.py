import os
import json
from pathlib import Path

original_path = Path(r"C:\Workspaces\fundetaxcol_flutter")
new_path = Path(r"C:\Workspaces\synergia_movil")

def scan_files(root: Path):
    if not root.exists():
        return {}
    res = {}
    for p in root.rglob("*.dart"):
        rel = p.relative_to(root).as_posix()
        try:
            res[rel] = p.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            res[rel] = f"ERROR: {e}"
    return res

print("Scanning original project...")
orig_files = scan_files(original_path / "lib")
print(f"Original project has {len(orig_files)} dart files.")

print("Scanning new project...")
new_files = scan_files(new_path / "lib")
print(f"New project has {len(new_files)} dart files.")

print("\n--- ORIGINAL DART FILES ---")
for f in sorted(orig_files.keys()):
    print(f"  {f} ({len(orig_files[f].splitlines())} lines)")

print("\n--- NEW DART FILES ---")
for f in sorted(new_files.keys()):
    print(f"  {f} ({len(new_files[f].splitlines())} lines)")
