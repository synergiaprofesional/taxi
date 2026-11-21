import paramiko

def inspect_fundetaxcol():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Conectando a {host} para auditoría completa de servicios, timezone y módulos...")
    ssh.connect(host, username=user, password=password, timeout=10)

    commands = [
        ("1. Zona Horaria del Servidor y Fecha", "timedatectl; date; cat /etc/timezone 2>/dev/null; ls -l /etc/localtime"),
        ("2. Zona Horaria en PostgreSQL", "su - postgres -c \"psql -d fundetaxcol -c 'SHOW timezone;' -c 'SELECT name, tz FROM res_users LIMIT 5;' -c 'SELECT id, name, partner_id FROM res_company;'\" 2>/dev/null || echo 'Postgres tz query omitida'"),
        ("3. Todos los servicios systemd en /etc/systemd/system/", "ls -la /etc/systemd/system/ | grep -E '(odoo|socket|node|fundetax|taxi|bahia|turn|serv|proxy|synergia)'"),
        ("4. Contenido de los servicios encontrados", "cat /etc/systemd/system/socket* 2>/dev/null || cat /etc/systemd/system/*node* 2>/dev/null || echo 'No socket service in systemd'"),
        ("5. Procesos y Puertos adicionales escuchando (incluyendo node/socket)", "ps aux | grep -E '(node|socket|pm2|odoo|python)' | grep -v grep; echo '--- Puertos ---'; netstat -tulpn"),
        ("6. Directorio /opt/synergia y sus carpetas", "ls -la /opt/synergia/"),
        ("7. Contenido de /opt/synergia/addons_fundetaxcol", "ls -la /opt/synergia/addons_fundetaxcol/"),
        ("8. Servicios habilitados en systemctl", "systemctl list-unit-files --state=enabled | grep -E '(odoo|node|socket|synergia|fundetax)' || echo 'No enabled specific units'")
    ]

    for title, cmd in commands:
        print(f"\n=======================================================")
        print(f"=== {title} ===")
        print(f"=======================================================")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore').strip()
        print(out)

    ssh.close()

if __name__ == "__main__":
    inspect_fundetaxcol()
