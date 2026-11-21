import os

for fname in ['config.conf', 'Caddyfile', 'main.py', 'server_hybrid.py']:
    fp = os.path.join(r"C:\proxyServer", fname)
    if os.path.exists(fp):
        print(f"\n=================== {fname} ===================")
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            print(f.read()[:2000])
