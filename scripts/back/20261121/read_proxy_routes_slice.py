with open(r"C:\proxyServer\src\routes.py", 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def _register_routes' in l:
        print("".join(lines[i:i+30]))
        break
