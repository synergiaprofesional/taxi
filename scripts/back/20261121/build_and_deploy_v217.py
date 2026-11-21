import subprocess
import os
import sys
import time

def log(msg):
    print(f"[DEPLOY-v217] {msg}", flush=True)

adb_path = r"C:\Users\salis\AppData\Local\Android\Sdk\platform-tools\adb.exe"

# 0. Cerrar proceso previo de synergia_movil si está corriendo para desbloquear el binario en Windows
subprocess.run("taskkill /F /IM synergia_movil.exe 2>nul", shell=True)
time.sleep(1)

# 1. Preparar Windows Release
exe_path = r"build\windows\x64\runner\Release\synergia_movil.exe"
if os.path.exists(exe_path):
    try:
        os.remove(exe_path)
        log(f"Ejecutable previo eliminado: {exe_path}")
    except Exception as e:
        log(f"Aviso al eliminar {exe_path}: {e}")

runner_cpp = r"windows\runner\main.cpp"
if os.path.exists(runner_cpp):
    os.utime(runner_cpp, None)

log("Iniciando compilacion Flutter Windows Release...")
ret_win = subprocess.run("flutter build windows --release", shell=True)
if ret_win.returncode != 0:
    log("ERROR: Fallo compilacion Windows Release")
    sys.exit(1)

if os.path.exists(exe_path):
    mtime = os.path.getmtime(exe_path)
    size = os.path.getsize(exe_path)
    log(f"GATE WINDOWS EXITOSO: {exe_path} | Size: {size} bytes | mtime: {time.ctime(mtime)}")
else:
    log("ERROR: No se encontro synergia_movil.exe")
    sys.exit(1)

# 2. Compilar APK Release
log("Iniciando compilacion Flutter APK Release (v2.1.7+9)...")
ret_apk = subprocess.run("flutter build apk --release", shell=True)
if ret_apk.returncode != 0:
    log("ERROR: Fallo compilacion APK Release")
    sys.exit(1)

apk_path = r"build\app\outputs\flutter-apk\app-release.apk"
if os.path.exists(apk_path):
    mtime_apk = os.path.getmtime(apk_path)
    size_apk = os.path.getsize(apk_path) / (1024 * 1024)
    log(f"GATE APK EXITOSO: {apk_path} | Size: {size_apk:.2f} MB | mtime: {time.ctime(mtime_apk)}")
else:
    log("ERROR: No se encontro app-release.apk")
    sys.exit(1)

# 3. Despliegue en tablet conectada via ADB
log("Verificando dispositivo Android por ADB...")
res_dev = subprocess.run(f'"{adb_path}" devices', shell=True, capture_output=True, text=True)
print(res_dev.stdout)

target_device = "HA27VLYC"
log(f"Instalando APK v2.1.7 en tablet {target_device}...")
ret_inst = subprocess.run(f'"{adb_path}" -s {target_device} install -r {apk_path}', shell=True)
if ret_inst.returncode == 0:
    log("Lanzando app en primer plano en la tablet...")
    subprocess.run(f'"{adb_path}" -s {target_device} shell am start -n com.synergia.synergia_movil/.MainActivity', shell=True)
    log("Verificando paquete instalado con dumpsys...")
    dumpsys = subprocess.run(f'"{adb_path}" -s {target_device} shell dumpsys package com.synergia.synergia_movil', shell=True, capture_output=True, text=True)
    for line in dumpsys.stdout.splitlines():
        if "versionName" in line or "lastUpdateTime" in line:
            print("   ", line.strip())
else:
    log("Fallo instalacion por ADB")
