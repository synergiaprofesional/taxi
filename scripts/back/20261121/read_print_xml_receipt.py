with open(r"C:\proxyServer\src\routes.py", 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def print_xml_receipt(self):' in l:
        print("".join(lines[i:i+50]))
        break
