with open(r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\models\turno_model.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'vehiculo_ids' in line and 'fields.Many2many' not in line:
        start = max(0, i - 10)
        end = min(len(lines), i + 25)
        print(f"=== OCCURRENCE AT LINE {i+1} ===")
        print("".join(lines[start:end]))
