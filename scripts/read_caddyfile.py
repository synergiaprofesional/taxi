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

stdin, stdout, stderr = ssh.exec_command("cat /opt/synergia/docker/Caddyfile")
print("=== Contenido de /opt/synergia/docker/Caddyfile ===")
print(stdout.read().decode())
ssh.close()
