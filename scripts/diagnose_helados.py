import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("SERVER_HOST", "80.190.75.49")
user = os.getenv("SERVER_USER", "root")
password = os.getenv("SERVER_PASS", "")
port = int(os.getenv("SERVER_PORT", "22"))

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port=port, username=user, password=password, timeout=12)

def run(cmd):
    print(f"=== {cmd} ===")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    if out: print(out)
    if err: print("ERR:", err)

run("grep -A 10 'helados.synergiapos.co' /opt/synergia/docker/Caddyfile")
run("curl -k -I https://localhost -H 'Host: helados.synergiapos.co'")
run("docker logs --tail 30 helados-helados-1")
run("docker logs --tail 30 docker-caddy-1")

ssh.close()
