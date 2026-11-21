import os
import time

p = r"c:\Workspaces\synergia_movil\build\windows\x64\runner\Release\data\app.so"
if os.path.exists(p):
    print("app.so mtime:", time.ctime(os.path.getmtime(p)))
    print("app.so size:", os.path.getsize(p))
else:
    print("app.so not found")

# List all files in Release dir
rel_dir = r"c:\Workspaces\synergia_movil\build\windows\x64\runner\Release"
for root, dirs, files in os.walk(rel_dir):
    for f in files:
        fp = os.path.join(root, f)
        print(f"{time.ctime(os.path.getmtime(fp))} | {os.path.getsize(fp):>10} | {os.path.relpath(fp, rel_dir)}")
