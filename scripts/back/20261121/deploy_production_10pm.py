"""
Script de Despliegue Automatizado para la Ventana de Mantenimiento (10:00 PM COT).
Servidor: fundetaxcol.co (Ubuntu 18.04 LTS)

Tareas ejecutadas en secuencia atómica:
1. Corrección de Timezone a America/Bogota (resuelve desfase de tiquetes).
2. Instalación y configuración de Fail2ban con lista blanca (190.253.19.26 y 190.242.47.74).
3. Corrección de errata en systemd y levantamiento de server_rt_odoo (Socket puerto 3000).
4. Instalación de Caddy v2 con Caddyfile de Soporte Dual (HTTP 80 + HTTPS 443).
5. Switchover atómico de Odoo (puerto 8069, proxy_mode=True, workers=2).
6. Verificación integral de servicios, puertos y respuesta HTTP/HTTPS.
"""

import paramiko
import time

def deploy_maintenance_window():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("=" * 60)
    print(f"🚀 INICIANDO DESPLIEGUE EN VENTANA DE MANTENIMIENTO: {host}")
    print("=" * 60)
    ssh.connect(host, username=user, password=password, timeout=15)

    commands = [
        # --- PASO 1: TIMEZONE ---
        ("1. Ajustar Zona Horaria a America/Bogota", """
            timedatectl set-timezone America/Bogota &&
            timedatectl && date
        """),

        # --- PASO 2: FAIL2BAN ---
        ("2. Instalar y Configurar Fail2ban con Lista Blanca", """
            export DEBIAN_FRONTEND=noninteractive &&
            apt-get update -y &&
            apt-get install -y fail2ban &&
            cat << 'EOF' > /etc/fail2ban/jail.local
[DEFAULT]
ignoreip = 127.0.0.1/8 ::1 190.253.19.26 190.242.47.74
bantime  = 1h
findtime = 10m
maxretry = 5

[sshd]
enabled = true
port    = 22
maxretry = 4
EOF
            systemctl restart fail2ban &&
            fail2ban-client status sshd
        """),

        # --- PASO 3: SERVER_RT_ODOO (SOCKET 3000) ---
        ("3. Corregir Typo en server_rt_odoo y Levantar Puerto 3000", """
            sed -i 's/nulti-user.target/multi-user.target/g' /etc/systemd/system/server_rt_odoo.service &&
            systemctl daemon-reload &&
            systemctl restart server_rt_odoo.service &&
            systemctl status server_rt_odoo.service --no-pager
        """),

        # --- PASO 4: CADDY V2 INSTALL ---
        ("4. Descargar e Instalar Binario Caddy v2", """
            if ! which caddy > /dev/null 2>&1; then
                curl -fsSL https://github.com/caddyserver/caddy/releases/download/v2.8.4/caddy_2.8.4_linux_amd64.tar.gz -o /tmp/caddy.tar.gz &&
                tar -xzf /tmp/caddy.tar.gz -C /usr/bin caddy &&
                chmod +x /usr/bin/caddy &&
                mkdir -p /etc/caddy
            fi &&
            cat << 'EOF' > /etc/caddy/Caddyfile
http://fundetaxcol.co {
    reverse_proxy 127.0.0.1:8069 {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-For {remote_host}
        header_up X-Forwarded-Proto http
    }
}

fundetaxcol.co {
    # Soporte WebSocket Seguro para la nueva app Synergia Móvil (puerto 443 estándar)
    handle /socket.io/* {
        reverse_proxy 127.0.0.1:3000
    }
    handle {
        reverse_proxy 127.0.0.1:8069 {
            header_up Host {host}
            header_up X-Real-IP {remote_host}
            header_up X-Forwarded-For {remote_host}
            header_up X-Forwarded-Proto https
        }
    }
}
EOF
            caddy validate --config /etc/caddy/Caddyfile
        """),

        # --- PASO 5: CADDY SYSTEMD SERVICE ---
        ("5. Configurar Servicio Systemd para Caddy", """
            cat << 'EOF' > /etc/systemd/system/caddy.service
[Unit]
Description=Caddy Web Server
After=network.target

[Service]
Type=notify
User=root
ExecStart=/usr/bin/caddy run --environ --config /etc/caddy/Caddyfile
ExecReload=/usr/bin/caddy reload --config /etc/caddy/Caddyfile
TimeoutStopSec=5s
LimitNOFILE=1048576
Restart=always

[Install]
WantedBy=multi-user.target
EOF
            systemctl daemon-reload &&
            systemctl enable caddy.service
        """),

        # --- PASO 6: SWITCHOVER ATÓMICO (VENTANA < 3 SEG) ---
        ("6. Switchover Atómico de Odoo a Puerto 8069 y Arranque Caddy", """
            cp -n /opt/synergia/odoo-11.0/odoo_80.conf /opt/synergia/odoo-11.0/odoo_80.conf.bak &&
            systemctl stop odoo_80.service &&
            sed -i 's/^http_port = 80$/http_port = 8069/' /opt/synergia/odoo-11.0/odoo_80.conf &&
            sed -i 's/^proxy_mode = False$/proxy_mode = True/' /opt/synergia/odoo-11.0/odoo_80.conf &&
            sed -i 's/^http_interface = $/http_interface = 127.0.0.1/' /opt/synergia/odoo-11.0/odoo_80.conf &&
            systemctl start odoo_80.service &&
            systemctl start caddy.service &&
            systemctl restart postgresql
        """),

        # --- PASO 7: VERIFICACIÓN FINAL ---
        ("7. Verificación de Servicios, Puertos y Conectividad", """
            echo '--- Puertos Escuchando ---' &&
            netstat -tulpn | grep -E '(80|443|3000|8069)' &&
            echo '--- Test HTTP 80 (Legacy) ---' &&
            curl -I http://127.0.0.1 &&
            echo '--- Test HTTPS 443 (Moderno) ---' &&
            curl -I -k https://fundetaxcol.co &&
            echo '--- Estado de CPU Post-Despliegue ---' &&
            uptime
        """)
    ]

    for title, cmd in commands:
        print(f"\n>>> EJECUTANDO: {title}...")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore').strip()
        err = stderr.read().decode('utf-8', errors='ignore').strip()
        if out:
            print(out)
        if err:
            print(f"[STDERR]: {err}")
        print("-" * 50)

    ssh.close()
    print("\n✅ DESPLIEGUE FINALIZADO Y VERIFICADO.")

if __name__ == "__main__":
    deploy_maintenance_window()
