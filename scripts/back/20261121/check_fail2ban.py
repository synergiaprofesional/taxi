import paramiko

def check_fail2ban():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Verificando estado de Fail2ban en {host}...")
    ssh.connect(host, username=user, password=password, timeout=10)

    commands = [
        ("Verificar Fail2ban instalado", "which fail2ban-client || echo 'fail2ban NO instalado'"),
        ("Estado de servicio fail2ban", "systemctl status fail2ban 2>/dev/null || echo 'Servicio fail2ban no existe'"),
        ("Verificar jail.local existente", "ls -la /etc/fail2ban/jail* 2>/dev/null || echo 'No hay archivos de fail2ban'")
    ]

    for title, cmd in commands:
        print(f"\n=== {title} ===")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore').strip()
        print(out)

    ssh.close()

if __name__ == "__main__":
    check_fail2ban()
