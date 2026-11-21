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

stdin, stdout, stderr = ssh.exec_command("docker network ls")
print("=== Redes Docker en VPS ===")
print(stdout.read().decode())

stdin, stdout, stderr = ssh.exec_command("docker inspect docker-caddy-1 --format '{{json .NetworkSettings.Networks}}'")
print("=== Redes a las que está conectado docker-caddy-1 ===")
print(stdout.read().decode())

ssh.close()
