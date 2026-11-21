import os
import time
import subprocess

# 1. Check exe
exe_path = r"c:\Workspaces\synergia_movil\build\windows\x64\runner\Release\synergia_movil.exe"
if os.path.exists(exe_path):
    mtime = os.path.getmtime(exe_path)
    size = os.path.getsize(exe_path)
    print(f"EXE: {exe_path}")
    print(f"  Size: {size:,} bytes")
    print(f"  Last Modified: {time.ctime(mtime)} ({mtime})")
else:
    print("EXE NOT FOUND at", exe_path)

# 2. Check apk
apk_path = r"c:\Workspaces\synergia_movil\build\app\outputs\flutter-apk\app-release.apk"
if os.path.exists(apk_path):
    mtime = os.path.getmtime(apk_path)
    size = os.path.getsize(apk_path)
    print(f"APK: {apk_path}")
    print(f"  Size: {size:,} bytes")
    print(f"  Last Modified: {time.ctime(mtime)} ({mtime})")
else:
    print("APK NOT FOUND at", apk_path)

# 3. Check ADB installed package on device
adb_path = r"C:\Users\salis\AppData\Local\Android\Sdk\platform-tools\adb.exe"
res = subprocess.run([adb_path, "shell", "pm", "list", "packages", "-3"], capture_output=True, text=True)
print("\nADB Third-party packages on device:")
print(res.stdout)

# Check specifically for synergia
res_syn = subprocess.run([adb_path, "shell", "pm", "dump", "com.synergia.movil"], capture_output=True, text=True)
for line in res_syn.stdout.splitlines():
    if "versionName" in line or "versionCode" in line or "firstInstallTime" in line or "lastUpdateTime" in line:
        print(line.strip())
