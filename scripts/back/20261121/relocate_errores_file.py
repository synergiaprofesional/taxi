import shutil
import os

workspace = r"c:\Workspaces\synergia_movil"
src = os.path.join(workspace, "docs", "errores.md")
dst = os.path.join(workspace, "ERRORES.md")

if os.path.exists(src):
    shutil.move(src, dst)
    print(f"MOVED: {src} -> {dst}")
    print(f"Exists in destination: {os.path.exists(dst)}")
    print(f"Size: {os.path.getsize(dst)} bytes")
else:
    print(f"Source file not found: {src}")
