import subprocess
import sys

print("[ANALYZE] Ejecutando flutter analyze...", flush=True)
res = subprocess.run("cmd.exe /c flutter analyze", shell=True, capture_output=True, text=True)
print(res.stdout, flush=True)
if res.stderr:
    print(res.stderr, file=sys.stderr, flush=True)
sys.exit(res.returncode)

