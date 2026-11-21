import os

routes_fp = r"C:\proxyServer\src\routes.py"
if os.path.exists(routes_fp):
    with open(routes_fp, 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read())
else:
    print("No se encontró routes.py")
