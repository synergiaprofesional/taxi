with open(r"C:\proxyServer\src\routes.py", 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

import re
matches = re.findall(r'.{0,50}win32print.{0,50}', c)
for m in matches[:10]:
    print(m.strip())
