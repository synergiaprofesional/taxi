with open(r"C:\proxyServer\src\routes.py", 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def run(self):' in l or 'def push_task(' in l or 'def _html_to_pdf(' in l:
        start = max(0, i - 2)
        end = min(len(lines), i + 40)
        print("".join(lines[start:end]))
        print("="*60)
