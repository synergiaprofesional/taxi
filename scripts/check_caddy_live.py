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

stdin, stdout, stderr = ssh.exec_command("docker logs --tail 25 docker-caddy-1")
print("=== Logs de Caddy ===")
print(stdout.read().decode())
print(stderr.read().decode())

stdin, stdout, stderr = ssh.exec_command("curl -I http://localhost -H 'Host: pidemeaqui.com'")
print("=== Prueba Local HTTP en VPS ===")
print(stdout.read().decode())
print(stderr.read().decode())

ssh.close()
