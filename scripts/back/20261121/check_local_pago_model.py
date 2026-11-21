import os

def check_models():
    models_dir = r"C:\Workspaces\addons_fundetaxcol\fundetaxcol\models"
    for fname in os.listdir(models_dir):
        if fname.endswith(".py"):
            fpath = os.path.join(models_dir, fname)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "fundetaxcol.pago" in content or "vehiculo" in content:
                    print(f"File {fname}:")
                    for line in content.splitlines():
                        if "Many2many" in line or "vehiculo" in line:
                            print(f"  {line.strip()}")

if __name__ == '__main__':
    check_models()
