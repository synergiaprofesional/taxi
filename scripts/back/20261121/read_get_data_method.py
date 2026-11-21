with open(r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\models\turno_model.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def get_data(self):' in line:
        start = max(0, i)
        end = min(len(lines), i + 30)
        print("".join(lines[start:end]))
        break
