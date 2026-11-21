import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(
    os.getenv("SERVER_HOST"),
    port=int(os.getenv("SERVER_PORT", "22")),
    username=os.getenv("SERVER_USER"),
    password=os.getenv("SERVER_PASS"),
    timeout=10
)

# 1. Inspeccionar montajes del contenedor docker-caddy-1
print("=== Inspeccionando montajes de docker-caddy-1 ===")
stdin, stdout, stderr = ssh.exec_command("docker inspect docker-caddy-1 --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}'")
print(stdout.read().decode())

# 2. Buscar archivos Caddyfile en el sistema
print("=== Buscando Caddyfile en el host ===")
stdin, stdout, stderr = ssh.exec_command("find /root /opt /home /etc -name 'Caddyfile' 2>/dev/null")
print(stdout.read().decode())

ssh.close()
