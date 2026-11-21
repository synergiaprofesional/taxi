with open(r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\models\vehiculo_model.py', 'r', encoding='utf-8') as f:
    content = f.read()
print(content[:3000])
if len(content) > 3000:
    print("\n--- NEXT PART ---\n")
    print(content[3000:6000])
