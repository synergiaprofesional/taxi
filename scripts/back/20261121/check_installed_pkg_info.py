import subprocess

adb_path = r"C:\Users\salis\AppData\Local\Android\Sdk\platform-tools\adb.exe"

for pkg in ["com.synergia.synergia_movil", "com.fundetaxcolapp"]:
    print(f"=== CHECKING {pkg} ===")
    res = subprocess.run([adb_path, "shell", "dumpsys", "package", pkg], capture_output=True, text=True)
    for line in res.stdout.splitlines():
        if "versionName" in line or "versionCode" in line or "firstInstallTime" in line or "lastUpdateTime" in line:
            print(" ", line.strip())
