import paramiko

def inspect_details():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=password, timeout=10)

    commands = [
        ("Caddyfile", "cat /etc/caddy/Caddyfile 2>/dev/null || cat /etc/Caddyfile 2>/dev/null"),
        ("Server RT Odoo dir", "ls -la /opt/server_rt_odoo/"),
        ("Server RT Odoo package.json", "cat /opt/server_rt_odoo/package.json 2>/dev/null || true"),
        ("Addons fundetaxcol modules", "ls -la /opt/synergia/addons_fundetaxcol/"),
        ("fundetaxcol_movil content", "ls -la /opt/synergia/addons_fundetaxcol/fundetaxcol_movil/ 2>/dev/null"),
        ("Odoo 80 config", "cat /opt/synergia/odoo-11.0/odoo_80.conf 2>/dev/null || true"),
    ]

    for title, cmd in commands:
        print(f"=== {title} ===")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore').strip()
        print(out if out else "[Vacio]")
        print("\n")

    ssh.close()

if __name__ == "__main__":
    inspect_details()
