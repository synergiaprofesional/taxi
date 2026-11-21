import os

js_path = r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\static\src\js\__print_ticket_client.js'
if os.path.exists(js_path):
    with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read())
else:
    print("Not found")
