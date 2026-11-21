import os

proxy_dir = r"C:\proxyServer"
if os.path.exists(proxy_dir):
    print(f"Archivos en {proxy_dir}:")
    for root, dirs, files in os.walk(proxy_dir):
        for f in files:
            fp = os.path.join(root, f)
            print(f" - {fp} ({os.path.getsize(fp)} bytes)")
else:
    print(f"No existe el directorio {proxy_dir}")
