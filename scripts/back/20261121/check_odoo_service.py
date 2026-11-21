import paramiko

def check_odoo_service():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Consultando servicio odoo_80 en {host}...")
    ssh.connect(host, username=user, password=password, timeout=10)

    commands = [
        ("Definición odoo_80.service", "systemctl cat odoo_80.service"),
        ("Comprobación Caddy instalado", "which caddy || echo 'Caddy no esta instalado'")
    ]

    for title, cmd in commands:
        print(f"\n=== {title} ===")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore').strip()
        print(out)

    ssh.close()

if __name__ == "__main__":
    check_odoo_service()
