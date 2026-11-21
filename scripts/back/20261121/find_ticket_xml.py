import os

addons_path = r'C:\Workspaces\addons_fundetaxcol'
for root, dirs, files in os.walk(addons_path):
    for f in files:
        if f.endswith('.xml'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fl:
                c = fl.read()
                if 'ticket_client' in c:
                    print("Found in XML:", fp)
                    lines = c.splitlines()
                    for idx, l in enumerate(lines):
                        if 'ticket_client' in l:
                            start = max(0, idx - 2)
                            end = min(len(lines), idx + 50)
                            print("\n".join(lines[start:end]))
                            break
