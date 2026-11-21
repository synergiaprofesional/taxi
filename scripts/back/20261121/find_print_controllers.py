import os

addons_path = r'C:\Workspaces\addons_fundetaxcol'
for root, dirs, files in os.walk(addons_path):
    for f in files:
        if f.endswith('.py'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fl:
                c = fl.read()
                if '/print/ticket_client' in c:
                    print("Found in:", fp)
                    lines = c.splitlines()
                    for idx, l in enumerate(lines):
                        if '/print/ticket_client' in l:
                            start = max(0, idx - 5)
                            end = min(len(lines), idx + 35)
                            print("\n".join(lines[start:end]))
