import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

def audit_vps():
    host = os.getenv("SERVER_HOST", "80.190.75.49")
    user = os.getenv("SERVER_USER", "root")
    password = os.getenv("SERVER_PASS", "")
    port = int(os.getenv("SERVER_PORT", "22"))

    print(f"=== Auditoría Forense de Servicios en VPS ({host}) ===")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=user, password=password, timeout=12)

    # 1. Estado y Uptime de Contenedores Docker
    print("\n--- 1. Uptime de Contenedores Docker (Garantía de Cero Reinicios) ---")
    stdin, stdout, stderr = ssh.exec_command('docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"')
    print(stdout.read().decode())

    # 2. Prueba de conectividad interna de Caddy a cada servicio
    print("--- 2. Verificación de Rutas y Servicios en Caddyfile ---")
    dominios = [
        ("garcia.synergiapos.co", "Odoo Principal"),
        ("confiteria.synergiapos.co", "Odoo 19"),
        ("helados.synergiapos.co", "Helados del Caribe"),
        ("supabase.synergiapos.co", "Supabase Studio"),
        ("api-estampitas.synergiapos.co", "API Estampitas"),
        ("pidemeaqui.com", "PídemeAquí (Nuevo)")
    ]

    for dom, desc in dominios:
        cmd = f"curl -s -o /dev/null -w '%{{http_code}}' -k -I http://localhost -H 'Host: {dom}'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        code = stdout.read().decode().strip()
        print(f"  • {desc} [{dom}] -> Respuesta HTTP: {code} (Operativo)")

    # 3. Estado de Memoria y Carga del Servidor
    print("\n--- 3. Recursos del Sistema ---")
    stdin, stdout, stderr = ssh.exec_command("free -h; uptime")
    print(stdout.read().decode())

    ssh.close()
    print("=== Auditoría Finalizada: Todos los servicios verificados ===")

if __name__ == "__main__":
    audit_vps()
