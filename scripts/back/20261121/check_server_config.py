import paramiko

def check_server():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Conectando a {host}...")
    ssh.connect(host, username=user, password=password, timeout=10)
    print("Conexión SSH exitosa.\n")

    commands = [
        ("Uptime y Sistema", "uptime; uname -a"),
        ("Puertos escuchando", "ss -tulpn | grep -E '(80|443|3000|8069)'"),
        ("Configuración Nginx", "ls -la /etc/nginx/sites-enabled/ 2>/dev/null || echo 'No nginx sites'"),
        ("Detalle Nginx Default/Sitios", "cat /etc/nginx/sites-enabled/* 2>/dev/null || cat /etc/nginx/conf.d/* 2>/dev/null || echo 'No configs'"),
        ("Servicios de Odoo y Socket", "systemctl list-units --type=service --state=running | grep -E '(odoo|node|socket|pm2)' || ps aux | grep -E '(odoo|python|node)' | grep -v grep")
    ]

    for title, cmd in commands:
        print(f"=== {title} ===")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore').strip()
        err = stderr.read().decode('utf-8', errors='ignore').strip()
        if out:
            print(out)
        if err:
            print(f"[STDERR]: {err}")
        print("\n")

    ssh.close()

if __name__ == "__main__":
    check_server()
