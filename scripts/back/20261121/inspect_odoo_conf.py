import paramiko

def inspect_odoo_conf():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Conectando a {host} para inspeccionar odoo_80.conf...")
    ssh.connect(host, username=user, password=password, timeout=10)

    commands = [
        ("Contenido odoo_80.conf", "cat /opt/synergia/odoo-11.0/odoo_80.conf"),
        ("Version de Ubuntu", "cat /etc/os-release | grep -E '(NAME|VERSION)'"),
        ("Verificar puertos en uso", "netstat -tulpn | grep LISTEN")
    ]

    for title, cmd in commands:
        print(f"\n=== {title} ===")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore').strip()
        print(out)

    ssh.close()

if __name__ == "__main__":
    inspect_odoo_conf()
