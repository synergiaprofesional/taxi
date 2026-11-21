import paramiko

def inspect():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Conectando en MODO SOLO CONSULTA a {host}...")
    ssh.connect(host, username=user, password=password, timeout=10)
    print("Conexión SSH exitosa (READ-ONLY).\n")

    queries = [
        ("Estructura en /opt", "ls -la /opt 2>/dev/null"),
        ("Estructura en /var/www", "ls -la /var/www 2>/dev/null"),
        ("Estructura en /root", "ls -la /root 2>/dev/null"),
        ("Estructura /home", "ls -la /home 2>/dev/null"),
        ("Servicios activos (systemd / pm2)", "systemctl list-units --type=service --state=running | grep -E '(odoo|node|socket|pm2|caddy|nginx)'"),
        ("Puertos activos", "ss -tulpn | grep -E '(80|443|3000|8069|5000|8080)'"),
        ("Buscar directorios de fundetaxcol o synergia", "find /opt /var/www /root -maxdepth 3 -iname '*fundetaxcol*' -o -iname '*synergia*' -o -iname '*server_rt*' 2>/dev/null"),
        ("Addons Odoo en el servidor", "find /opt -maxdepth 3 -name 'addons*' 2>/dev/null")
    ]

    for title, cmd in queries:
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
    inspect()
