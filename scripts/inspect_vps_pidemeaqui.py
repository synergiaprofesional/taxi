import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

def inspect_vps():
    host = os.getenv("SERVER_HOST", "80.190.75.49")
    user = os.getenv("SERVER_USER", "root")
    password = os.getenv("SERVER_PASS", "")
    port = int(os.getenv("SERVER_PORT", "22"))
    domain = os.getenv("DOMAIN_NAME", "pidemeaqui.com")

    print(f"=== Inspección de VPS Destino para {domain} ===")
    print(f"Conectando a {user}@{host}:{port}...\n")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port=port, username=user, password=password, timeout=12)
        print("✅ Conexión SSH establecida con éxito al nuevo VPS.\n")
    except Exception as e:
        print(f"❌ Error al conectar al VPS: {e}")
        return

    queries = [
        ("Sistema Operativo", "cat /etc/os-release | grep -E '^(PRETTY_NAME|VERSION)='"),
        ("Arquitectura y Kernel", "uname -mrs"),
        ("Memoria RAM", "free -h"),
        ("Espacio en Disco", "df -h /"),
        ("Puertos en Escucha", "ss -tulpn | grep -E ':(80|443|22|3000|8080|5000)'"),
        ("Servidores Web / Proxies", "systemctl list-units --type=service --state=running | grep -E '(nginx|caddy|apache|docker)'"),
        ("Versiones de Runtimes", "node -v 2>/dev/null || echo 'Node: no instalado'; python3 -V 2>/dev/null || echo 'Python3: no instalado'; docker -v 2>/dev/null || echo 'Docker: no instalado'"),
        ("Estructura Web / Directorios", "ls -la /var/www 2>/dev/null || echo '/var/www no existe'")
    ]

    for title, cmd in queries:
        print(f"--- {title} ---")
        try:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = stdout.read().decode('utf-8', errors='ignore').strip()
            err = stderr.read().decode('utf-8', errors='ignore').strip()
            if out:
                print(out)
            if err:
                print(f"[Aviso/Err]: {err}")
        except Exception as e:
            print(f"Error ejecutando '{cmd}': {e}")
        print()

    ssh.close()
    print("=== Inspección de VPS finalizada ===")

if __name__ == "__main__":
    inspect_vps()
