with open(r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\static\src\xml\fundetaxcol.xml', 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

idx = c.find('fundetaxcol.print.cliente')
if idx != -1:
    print(c[idx-50:idx+1500])
else:
    print("Not found")
