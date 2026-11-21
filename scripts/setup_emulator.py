import os
import sys
import zipfile
import subprocess
import urllib.request
import time

URL = "https://dl.google.com/android/repository/sys-img/google_apis/x86_64-34_r14.zip"
SDK_DIR = r"C:\Users\salis\AppData\Local\Android\Sdk"
TARGET_DIR = os.path.join(SDK_DIR, "system-images", "android-34", "google_apis", "x86_64")
ZIP_PATH = os.path.join(SDK_DIR, "x86_64-34_r14.zip")
AVD_NAME = "Taxi_Emulator"

def main():
    print("=== Configuración Automatizada de Emulador Android ===")
    os.makedirs(os.path.dirname(TARGET_DIR), exist_ok=True)
    
    # 1. Descarga con reintentos y reporte de progreso
    if not os.path.exists(ZIP_PATH) or os.path.getsize(ZIP_PATH) < 1500000000:
        print(f"Descargando imagen de sistema Android 34 (1.5 GB)...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(URL, headers=headers)
        
        with urllib.request.urlopen(req) as resp, open(ZIP_PATH, 'wb') as out_file:
            total_size = int(resp.headers.get('content-length', 0))
            downloaded = 0
            start_time = time.time()
            chunk_size = 4 * 1024 * 1024 # 4MB
            
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                out_file.write(chunk)
                downloaded += len(chunk)
                percent = int(downloaded * 100 / total_size) if total_size else 0
                mb = downloaded / (1024 * 1024)
                total_mb = total_size / (1024 * 1024)
                elapsed = time.time() - start_time
                speed = mb / elapsed if elapsed > 0 else 0
                print(f"\rDescargando: {mb:.1f}/{total_mb:.1f} MB ({percent}%) a {speed:.1f} MB/s", end='', flush=True)
        print("\nDescarga completada con éxito.")
    else:
        print("Archivo ZIP ya descargado previamente.")

    # 2. Descomprimir en TARGET_DIR
    print(f"Extrayendo imagen en {TARGET_DIR}...")
    os.makedirs(TARGET_DIR, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        # El zip contiene 'x86_64/...'
        for member in zip_ref.namelist():
            # Quitar prefijo si existe
            filename = member
            if filename.startswith("x86_64/"):
                filename = filename[7:]
            if not filename:
                continue
            dest_path = os.path.join(TARGET_DIR, filename)
            if member.endswith('/'):
                os.makedirs(dest_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with zip_ref.open(member) as src, open(dest_path, 'wb') as dst:
                    dst.write(src.read())
    print("Extracción completada.")

    # Eliminar zip para liberar espacio
    try:
        os.remove(ZIP_PATH)
    except:
        pass

    # 3. Crear AVD con avdmanager
    avdmanager = os.path.join(SDK_DIR, "cmdline-tools", "latest", "bin", "avdmanager.bat")
    cmd_create = f'echo no | "{avdmanager}" create avd -n "{AVD_NAME}" -k "system-images;android-34;google_apis;x86_64" --force'
    print(f"Creando AVD '{AVD_NAME}'...")
    subprocess.run(cmd_create, shell=True, check=True)
    print("AVD creado exitosamente.")

    # 4. Iniciar emulador
    emulator = os.path.join(SDK_DIR, "emulator", "emulator.exe")
    print(f"Iniciando emulador '{AVD_NAME}'...")
    subprocess.Popen([emulator, "-avd", AVD_NAME, "-netdelay", "none", "-netspeed", "full"])
    print("✅ Emulador Android iniciado en pantalla.")

if __name__ == "__main__":
    main()
