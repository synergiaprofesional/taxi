import paramiko
import json

def check_server_performance():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Conectando a {host} para auditoría de rendimiento y logs...")
    ssh.connect(host, username=user, password=password, timeout=10)

    commands = [
        ("1. CPU y Especificaciones de Hardware", "lscpu | grep -E 'Model name|CPU\(s\):|Thread|Core|BogoMIPS'; uptime"),
        ("2. Memoria RAM y Swap", "free -h; vmstat 1 3"),
        ("3. Espacio en Disco y Uso de I/O", "df -h / /var /opt; iostat -xz 1 2 2>/dev/null || echo 'iostat no disponible'"),
        ("4. Procesos Top por CPU y Memoria", "ps aux --sort=-%mem | head -n 12; echo '--- Top CPU ---'; ps aux --sort=-%cpu | head -n 10"),
        ("5. Métricas del Proceso Odoo (PID y consumo)", "ps -eo pid,ppid,cmd,%mem,%cpu,rss,vsz,nlwp --sort=-%mem | grep -E '(odoo|python)' | head -n 10"),
        ("6. Estado y Actividad de PostgreSQL", "su - postgres -c \"psql -c 'SELECT count(*) as total_connections FROM pg_stat_activity;' -c 'SELECT datname, numbackends, xact_commit, xact_rollback FROM pg_stat_database WHERE datname=\\'fundetaxcol\\';' -c 'SELECT pid, query_start, state, query FROM pg_stat_activity WHERE state != \\'idle\\' AND query NOT ILIKE \\'%pg_stat%\\';'\" 2>/dev/null || echo 'Postgres query directa omitida'"),
        ("7. Logs Recientes de odoo_80.service (Últimas 60 líneas)", "journalctl -u odoo_80.service -n 60 --no-pager 2>/dev/null || tail -n 60 /var/log/syslog | grep odoo"),
        ("8. Conteo de Errores y Warnings en Logs de Odoo", "journalctl -u odoo_80.service --since '24 hours ago' --no-pager 2>/dev/null | grep -E 'ERROR|CRITICAL|WARNING' | tail -n 25 || echo 'No errors in journalctl'")
    ]

    results = {}
    for title, cmd in commands:
        print(f"\n=======================================================")
        print(f"=== {title} ===")
        print(f"=======================================================")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore').strip()
        err = stderr.read().decode('utf-8', errors='ignore').strip()
        if out:
            print(out)
        if err:
            print(f"[STDERR]: {err}")
        results[title] = out

    ssh.close()
    return results

if __name__ == "__main__":
    check_server_performance()
