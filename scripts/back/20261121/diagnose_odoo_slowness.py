import paramiko
import re

def diagnose():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"[*] Conectando vía SSH a {host}...")
    ssh.connect(host, username=user, password=password, timeout=12)

    commands = [
        ("1. Carga actual de CPU, RAM y Uptime", "uptime; free -h; vmstat 1 3"),
        ("2. Configuración del servicio Odoo (Systemd & cmd)", "ps aux | grep -E '(odoo|python)' | grep -v grep; systemctl cat odoo_80.service 2>/dev/null || cat /etc/systemd/system/odoo* 2>/dev/null"),
        ("3. Archivos de configuración de Odoo (odoo.conf)", "find /etc /opt /home -name '*odoo*.conf' -type f 2>/dev/null -exec grep -H -E '(workers|limit_|timeout|logfile|log_level|db_|max_cron)' {} +"),
        ("4. Dónde están los archivos de log de Odoo y su tamaño", "ls -lh /var/log/odoo* /var/log/syslog /opt/synergia/*.log 2>/dev/null; find /var/log -name '*odoo*' -exec ls -lh {} + 2>/dev/null"),
        ("5. Últimas 100 líneas del log de Odoo (journalctl)", "journalctl -u odoo_80.service -n 100 --no-pager 2>/dev/null"),
        ("6. Detección de consultas lentas en el log (query > 1s o > 500ms)", "journalctl -u odoo_80.service --since '3 days ago' --no-pager 2>/dev/null | grep -E '(query|time|ms|s) in' | tail -n 30 || echo 'No time logs in journalctl'"),
        ("7. Errores, Tracebacks y Warnings críticos en Odoo", "journalctl -u odoo_80.service --since '24 hours ago' --no-pager 2>/dev/null | grep -E '(Traceback|ERROR|CRITICAL|Worker .* killed|Memory limit exceeded|timeout)' | tail -n 40"),
        ("8. Conexiones y consultas activas en PostgreSQL", "sudo -u postgres psql -d fundetaxcol -c \"SELECT pid, usename, client_addr, state, now() - query_start AS duration, query FROM pg_stat_activity WHERE state != 'idle' AND pid <> pg_backend_pid() ORDER BY duration DESC;\""),
        ("9. Tablas más grandes en PostgreSQL (registros y tamaño)", "sudo -u postgres psql -d fundetaxcol -c \"SELECT relname AS table_name, reltuples::bigint AS row_estimate, pg_size_pretty(pg_total_relation_size(c.oid)) AS total_size FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = 'public' AND c.relkind = 'r' ORDER BY pg_total_relation_size(c.oid) DESC LIMIT 20;\""),
        ("10. Índices y locks en PostgreSQL", "sudo -u postgres psql -d fundetaxcol -c \"SELECT blocked_locks.pid AS blocked_pid, blocked_activity.usename AS blocked_user, blocking_locks.pid AS blocking_pid, blocking_activity.usename AS blocking_user, blocked_activity.query AS blocked_statement FROM pg_catalog.pg_locks blocked_locks JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype AND blocking_locks.DATABASE IS NOT DISTINCT FROM blocked_locks.DATABASE AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid AND blocking_locks.pid != blocked_locks.pid JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid WHERE NOT blocked_locks.GRANTED;\""),
        ("11. Estado del servicio Node.js RT (server_rt_odoo puerto 3000)", "systemctl status server_rt_odoo 2>/dev/null || ps aux | grep -E '(node|rt_odoo)' | grep -v grep; journalctl -u server_rt_odoo -n 30 --no-pager 2>/dev/null"),
        ("12. Tráfico de red y conexiones activas a puertos 80, 443, 3000, 8069", "netstat -tulnp | grep -E '(80|443|3000|8069|5432)'; ss -s; netstat -an | awk '/:80 |:443 |:8069 |:3000 / {print $6}' | sort | uniq -c")
    ]

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
            print(f"[STDERR]: {err[:500]}")

    ssh.close()
    print("\n[*] Diagnóstico de servidor completado.")

if __name__ == '__main__':
    diagnose()
