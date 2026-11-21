with open(r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\models\pago_model.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [line for line in content.splitlines() if 'valor' in line or 'concepto_ids' in line]
print("Lines with valor or concepto_ids:")
for m in matches[:30]:
    print(m)
