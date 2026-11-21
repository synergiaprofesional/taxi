import os

proxy_dir = r"C:\proxyServer"
files = [f for f in os.listdir(proxy_dir) if os.path.isfile(os.path.join(proxy_dir, f))]
print("Archivos en la raíz de C:\\proxyServer:")
for f in files:
    print(f" - {f}")
