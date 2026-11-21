with open(r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\models\turno_model.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def broadcast' in line:
        start = max(0, i)
        end = min(len(lines), i + 35)
        print("".join(lines[start:end]))
        break
