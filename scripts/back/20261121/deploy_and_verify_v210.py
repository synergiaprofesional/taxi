import os
import time
import subprocess

# 1. Verify EXE timestamp
exe_path = r"c:\Workspaces\synergia_movil\build\windows\x64\runner\Release\synergia_movil.exe"
if os.path.exists(exe_path):
    mtime = os.path.getmtime(exe_path)
    size = os.path.getsize(exe_path)
    print(f"FRESH EXE: {exe_path}")
    print(f"  Size: {size:,} bytes")
    print(f"  Timestamp: {time.ctime(mtime)} (Current time: {time.ctime()})")
else:
    print("EXE NOT FOUND")

# 2. Verify APK timestamp
apk_path = r"c:\Workspaces\synergia_movil\build\app\outputs\flutter-apk\app-release.apk"
if os.path.exists(apk_path):
    mtime = os.path.getmtime(apk_path)
    size = os.path.getsize(apk_path)
    print(f"\nFRESH APK v2.1.0: {apk_path}")
    print(f"  Size: {size:,} bytes")
    print(f"  Timestamp: {time.ctime(mtime)}")
else:
    print("APK NOT FOUND")

# 3. Install via ADB and launch in foreground
adb_path = r"C:\Users\salis\AppData\Local\Android\Sdk\platform-tools\adb.exe"
print("\n--- INSTALANDO APK v2.1.0+2 VIA ADB ---")
res_inst = subprocess.run([adb_path, "install", "-r", apk_path], capture_output=True, text=True)
print("Install output:", res_inst.stdout.strip() or res_inst.stderr.strip())

print("\n--- LANZANDO APP EN PRIMER PLANO EN EL DISPOSITIVO ---")
res_start = subprocess.run([adb_path, "shell", "am", "start", "-n", "com.synergia.synergia_movil/.MainActivity"], capture_output=True, text=True)
print("Start output:", res_start.stdout.strip() or res_start.stderr.strip())

print("\n--- VERIFICANDO PACKAGE DUMP ---")
res_dump = subprocess.run([adb_path, "shell", "dumpsys", "package", "com.synergia.synergia_movil"], capture_output=True, text=True)
for line in res_dump.stdout.splitlines():
    if "versionName" in line or "versionCode" in line or "lastUpdateTime" in line:
        print(" ", line.strip())
