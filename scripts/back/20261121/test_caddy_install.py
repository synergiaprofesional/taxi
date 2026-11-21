import paramiko

def check_caddy_prep():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Verificando prerequisitos de Caddy en {host}...")
    ssh.connect(host, username=user, password=password, timeout=10)

    commands = [
        ("Arquitectura y Libc", "dpkg --print-architecture; ldd --version | head -n 1"),
        ("Curl y Wget", "which curl; which wget"),
        ("Comprobacion firewall ufw", "ufw status 2>/dev/null || iptables -L -n | grep -E '(80|443)' | head -n 5")
    ]

    for title, cmd in commands:
        print(f"\n=== {title} ===")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore').strip()
        print(out)

    ssh.close()

if __name__ == "__main__":
    check_caddy_prep()
