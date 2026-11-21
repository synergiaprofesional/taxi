with open(r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\models\turno_model.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [line for line in content.splitlines() if 'vehiculo_ids' in line]
print("Lines with vehiculo_ids:")
for m in matches:
    print(m)
