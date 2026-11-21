import paramiko
import time

def verify_and_vacuum():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

    print("=== 1. VERIFICAR ACTIVIDAD DE POSTGRESQL ===")
    cmd_act = "cd /tmp && sudo -u postgres psql -d fundetaxcol -c 'SELECT pid, age(clock_timestamp(), query_start), state, query FROM pg_stat_activity WHERE state != \x27idle\x27;'"
    _, stdout, _ = ssh.exec_command(cmd_act)
    print(stdout.read().decode('utf-8'))

    print("=== 2. EJECUTAR VACUUM ANALYZE LIMPIO (desde /tmp) ===")
    tables = [
        'fundetaxcol_bahia',
        'bus_bus',
        'fundetaxcol_settings_mobile',
        'fundetaxcol_turno',
        'ir_cron',
        'mail_mail',
        'mail_message'
    ]
    for table in tables:
        cmd_v = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c 'VACUUM ANALYZE {table};'"
        _, stdout, stderr = ssh.exec_command(cmd_v)
        out = stdout.read().decode('utf-8').strip()
        err = stderr.read().decode('utf-8').strip()
        print(f"VACUUM {table}: {out} | {err}")

    print("=== 3. ESTADÍSTICAS DE TUPLAS MUERTAS POST-VACUUM ===")
    cmd_dead = """cd /tmp && sudo -u postgres psql -d fundetaxcol -c "
    SELECT relname, n_dead_tup, n_live_tup, last_vacuum, last_autovacuum, last_analyze 
    FROM pg_stat_user_tables 
    WHERE relname IN ('fundetaxcol_bahia', 'bus_bus', 'fundetaxcol_settings_mobile', 'fundetaxcol_turno', 'ir_cron', 'mail_mail');"
    """
    _, stdout, _ = ssh.exec_command(cmd_dead)
    print(stdout.read().decode('utf-8'))

    print("=== 4. ESTADO DE CPU ACTUAL DE ODOO ===")
    cmd_cpu = "ps aux | grep odoo-bin | grep -v grep; uptime"
    _, stdout, _ = ssh.exec_command(cmd_cpu)
    print(stdout.read().decode('utf-8'))

    print("=== 5. LATENCIA HTTP A /web/login ===")
    for i in range(3):
        cmd_curl = "curl -o /dev/null -s -w 'HTTP %{http_code} | Total: %{time_total}s | Connect: %{time_connect}s\\n' http://127.0.0.1:80/web/login"
        _, stdout, _ = ssh.exec_command(cmd_curl)
        print(stdout.read().decode('utf-8').strip())
        time.sleep(1)

    ssh.close()

if __name__ == '__main__':
    verify_and_vacuum()
