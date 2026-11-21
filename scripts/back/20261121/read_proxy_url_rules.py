with open(r"C:\proxyServer\src\routes.py", 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'route' in line or 'add_url_rule' in line or 'def ' in line:
            print(f"{idx+1}: {line.strip()}")
