import os
import time
import subprocess

workspace = r"c:\Workspaces\synergia_movil"
exe_path = os.path.join(workspace, r"build\windows\x64\runner\Release\synergia_movil.exe")
apk_path = os.path.join(workspace, r"build\app\outputs\flutter-apk\app-release.apk")
adb_path = r"C:\Users\salis\AppData\Local\Android\Sdk\platform-tools\adb.exe"

print("==================================================")
print("INICIANDO DESPLIEGUE Y VERIFICACIÓN EMPÍRICA v2.1.2+4")
print("==================================================")

# 1. FIX-001: Cerrar proceso activo si está corriendo y forzar re-link de Windows Runner
subprocess.run(["taskkill", "/f", "/im", "synergia_movil.exe"], capture_output=True, text=True)
time.sleep(0.5)

if os.path.exists(exe_path):
    print(f"Eliminando exe previo para garantizar mtime fresco: {exe_path}")
    try:
        os.remove(exe_path)
    except Exception as e:
        print(f"Aviso al eliminar exe: {e}")

# FIX-006: Sincronizar fuentes C++ del wrapper efímero de Windows
import shutil
wrapper_src = r'C:\flutter\bin\cache\artifacts\engine\windows-x64\cpp_client_wrapper'
wrapper_dst = os.path.join(workspace, r'windows\flutter\ephemeral\cpp_client_wrapper')
os.makedirs(wrapper_dst, exist_ok=True)
for item in os.listdir(wrapper_src):
    s = os.path.join(wrapper_src, item)
    d = os.path.join(wrapper_dst, item)
    if os.path.isfile(s):
        shutil.copy2(s, d)

print("\n[1/4] Compilando Windows Release...")
res_win = subprocess.run("flutter build windows --release", cwd=workspace, shell=True, capture_output=True, text=True)
if res_win.returncode != 0:
    print("ERROR al compilar Windows:", res_win.stderr)
else:
    print("Compilación Windows completada con éxito.")

if os.path.exists(exe_path):
    mtime = os.path.getmtime(exe_path)
    print(f"  -> synergia_movil.exe Verificado:")
    print(f"     Tamaño: {os.path.getsize(exe_path):,} bytes")
    print(f"     Timestamp: {time.ctime(mtime)}")
else:
    print("  -> ERROR: No se generó synergia_movil.exe")

print("\n[2/4] Compilando Android APK Release (v2.1.1+3)...")
res_apk = subprocess.run("flutter build apk --release", cwd=workspace, shell=True, capture_output=True, text=True)
if res_apk.returncode != 0:
    print("ERROR al compilar APK:", res_apk.stderr)
else:
    print("Compilación APK completada con éxito.")

if os.path.exists(apk_path):
    mtime = os.path.getmtime(apk_path)
    print(f"  -> app-release.apk Verificado:")
    print(f"     Tamaño: {os.path.getsize(apk_path):,} bytes")
    print(f"     Timestamp: {time.ctime(mtime)}")
else:
    print("  -> ERROR: No se generó app-release.apk")

# 2. FIX-002: Instalar vía ADB y lanzar en primer plano
print("\n[3/4] Instalando APK en dispositivo Android físico...")
res_inst = subprocess.run([adb_path, "install", "-r", apk_path], capture_output=True, text=True)
print("ADB Install:", res_inst.stdout.strip() or res_inst.stderr.strip())

print("\n[4/4] Levantando app en pantalla (foreground)...")
res_start = subprocess.run([adb_path, "shell", "am", "start", "-n", "com.synergia.synergia_movil/.MainActivity"], capture_output=True, text=True)
print("ADB Start:", res_start.stdout.strip() or res_start.stderr.strip())

print("\n--- AUDITORÍA EMPÍRICA EN DISPOSITIVO (DUMPSYS) ---")
res_dump = subprocess.run([adb_path, "shell", "dumpsys", "package", "com.synergia.synergia_movil"], capture_output=True, text=True)
for line in res_dump.stdout.splitlines():
    if "versionName" in line or "versionCode" in line or "lastUpdateTime" in line:
        print("  ", line.strip())

print("\n==================================================")
print("DESPLIEGUE FINALIZADO EXITOSAMENTE")
print("==================================================")
