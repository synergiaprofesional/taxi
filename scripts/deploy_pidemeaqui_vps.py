import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

def deploy_pidemeaqui():
    host = os.getenv("SERVER_HOST", "80.190.75.49")
    user = os.getenv("SERVER_USER", "root")
    password = os.getenv("SERVER_PASS", "")
    port = int(os.getenv("SERVER_PORT", "22"))

    print(f"=== Desplegando pidemeaqui.com en VPS ({host}) ===")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=user, password=password, timeout=12)

    # 1. Crear directorios
    print("1. Creando directorios en /opt/pidemeaqui...")
    ssh.exec_command("mkdir -p /opt/pidemeaqui/html")

    # 2. Subir docker-compose.yml para pidemeaqui-web
    compose_content = """services:
  web:
    image: nginx:alpine
    container_name: pidemeaqui-web
    restart: unless-stopped
    volumes:
      - /opt/pidemeaqui/html:/usr/share/nginx/html:ro
      - /opt/pidemeaqui/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    networks:
      - docker_default

networks:
  docker_default:
    external: true
"""
    sftp = ssh.open_sftp()
    with sftp.file("/opt/pidemeaqui/docker-compose.yml", "w") as f:
        f.write(compose_content)

    # 3. Configuración Nginx para SPA / Routing
    nginx_conf = """server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg)$ {
        expires 7d;
        add_header Cache-Control "public, no-transform";
    }
}
"""
    with sftp.file("/opt/pidemeaqui/nginx.conf", "w") as f:
        f.write(nginx_conf)

    # 4. Subir la landing web de Taxi / PídemeAquí (leída de taxi_preview.html)
    with open("C:/Users/salis/.gemini/antigravity/brain/902547e2-2cf2-4477-a09a-e3d56e5fe87c/taxi_preview.html", "r", encoding="utf-8") as lf:
        landing_html = lf.read()

    with sftp.file("/opt/pidemeaqui/html/index.html", "w") as f:
        f.write(landing_html)

    sftp.close()
    print("2. Archivos subidos con éxito.")

    # 5. Levantar el contenedor pidemeaqui-web
    print("3. Levantando contenedor pidemeaqui-web...")
    stdin, stdout, stderr = ssh.exec_command("cd /opt/pidemeaqui && docker compose up -d")
    print(stdout.read().decode())
    print(stderr.read().decode())

    # 6. Actualizar /opt/synergia/docker/Caddyfile si no contiene pidemeaqui.com
    print("4. Verificando /opt/synergia/docker/Caddyfile...")
    stdin, stdout, stderr = ssh.exec_command("grep -q 'pidemeaqui.com' /opt/synergia/docker/Caddyfile && echo 'FOUND' || echo 'NOT_FOUND'")
    found = stdout.read().decode().strip()

    if found != "FOUND":
        print("Agregando bloque pidemeaqui.com a Caddyfile...")
        caddy_block = """

# PídemeAquí - Sistema Web y Tracking de Taxis
pidemeaqui.com {
	reverse_proxy pidemeaqui-web:80
}
"""
        stdin, stdout, stderr = ssh.exec_command(f"echo '{caddy_block}' >> /opt/synergia/docker/Caddyfile")
        print(stdout.read().decode())
    else:
        print("El bloque pidemeaqui.com ya existe en Caddyfile.")

    # 7. Recargar Caddy de forma limpia
    print("5. Recargando Caddy...")
    stdin, stdout, stderr = ssh.exec_command("docker exec docker-caddy-1 caddy reload --config /etc/caddy/Caddyfile")
    print(stdout.read().decode())
    print(stderr.read().decode())

    ssh.close()
    print("=== Despliegue completado ===")

if __name__ == "__main__":
    deploy_pidemeaqui()
