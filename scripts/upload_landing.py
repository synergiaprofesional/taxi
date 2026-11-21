import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

def deploy_landing():
    host = os.getenv("SERVER_HOST", "80.190.75.49")
    user = os.getenv("SERVER_USER", "root")
    password = os.getenv("SERVER_PASS", "")
    port = int(os.getenv("SERVER_PORT", "22"))

    print(f"=== Subiendo Landing Page Oficial a {host} ===")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=user, password=password, timeout=12)

    sftp = ssh.open_sftp()
    
    local_path = "c:/Workspaces/taxi/landing/index.html"
    remote_path = "/opt/pidemeaqui/html/index.html"
    
    print(f"Transfiriendo {local_path} -> {remote_path}...")
    sftp.put(local_path, remote_path)
    sftp.close()

    print("Recargando Nginx en contenedor pidemeaqui-web...")
    stdin, stdout, stderr = ssh.exec_command("docker exec pidemeaqui-web nginx -s reload")
    print(stdout.read().decode())
    print(stderr.read().decode())

    ssh.close()
    print("✅ Landing Page desplegada exitosamente en https://pidemeaqui.com")

if __name__ == "__main__":
    deploy_landing()
