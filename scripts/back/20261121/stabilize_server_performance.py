import paramiko

def stabilize_server():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

    print("=== 1. MATANDO TRANSACCIONES ZOMBI EN POSTGRESQL ===")
    kill_zombies_sql = """
    SELECT pg_terminate_backend(pid), pid, state, age(clock_timestamp(), state_change) 
    FROM pg_stat_activity 
    WHERE state = 'idle in transaction' 
       OR (state = 'idle' AND age(clock_timestamp(), state_change) > interval '1 day')
       OR age(clock_timestamp(), query_start) > interval '1 day';
    """
    cmd_kill = f"sudo -u postgres psql -d fundetaxcol -c \"{kill_zombies_sql}\""
    _, stdout, stderr = ssh.exec_command(cmd_kill)
    print(stdout.read().decode('utf-8'))

    print("=== 2. CORRIGIENDO CRON ID 2 (MAIL QUEUE MANAGER - INTERVALO 0 MIN) ===")
    # Ver cron 2 actual
    cmd_cron_before = "sudo -u postgres psql -d fundetaxcol -c \"SELECT id, name, interval_number, interval_type, active, nextcall FROM ir_cron WHERE id=2;\""
    _, stdout, _ = ssh.exec_command(cmd_cron_before)
    print("Antes:")
    print(stdout.read().decode('utf-8'))

    # Actualizar a 15 minutos y nextcall a futuro
    cmd_fix_cron = """
    sudo -u postgres psql -d fundetaxcol -c "UPDATE ir_cron SET interval_number = 15, interval_type = 'minutes', nextcall = (now() at time zone 'UTC') + interval '15 minutes' WHERE id = 2;"
    """
    _, stdout, _ = ssh.exec_command(cmd_fix_cron)
    print("Actualización:")
    print(stdout.read().decode('utf-8'))

    print("=== 3. EJECUTANDO VACUUM ANALYZE EN TABLAS CRÍTICAS ===")
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
        print(f"-> VACUUM ANALYZE {table}...")
        cmd_vacuum = f"sudo -u postgres psql -d fundetaxcol -c \"VACUUM ANALYZE {table};\""
        _, stdout, stderr = ssh.exec_command(cmd_vacuum)
        res = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        if err:
            print(f"Error: {err.strip()}")
        else:
            print(f"OK: {res.strip()}")

    print("=== 4. VERIFICANDO TUPLAS MUERTAS DESPUÉS DEL VACUUM ===")
    cmd_stats = "sudo -u postgres psql -d fundetaxcol -c 'SELECT relname, n_dead_tup, n_live_tup, last_vacuum, last_autovacuum, last_analyze FROM pg_stat_user_tables WHERE relname IN (\x27fundetaxcol_bahia\x27, \x27bus_bus\x27, \x27fundetaxcol_settings_mobile\x27, \x27fundetaxcol_turno\x27, \x27ir_cron\x27, \x27mail_mail\x27);'"
    _, stdout, _ = ssh.exec_command(cmd_stats)
    print(stdout.read().decode('utf-8'))

    print("=== 5. REINICIANDO ODOO_80.SERVICE PARA LIBERAR CPU DESTRABADA ===")
    cmd_restart = "systemctl restart odoo_80.service"
    _, stdout, stderr = ssh.exec_command(cmd_restart)
    stdout.channel.recv_exit_status()
    print("Servicio reiniciado.")

    print("=== 6. INSPECCIONANDO ESTADO Y CPU TRAS REINICIO ===")
    import time
    time.sleep(3)
    cmd_top = "ps aux | grep odoo | grep -v grep; uptime"
    _, stdout, _ = ssh.exec_command(cmd_top)
    print(stdout.read().decode('utf-8'))

    print("=== 7. PROBANDO LATENCIA HTTP EN PUERTO 80 ===")
    cmd_curl = "curl -o /dev/null -s -w 'HTTP Status: %{http_code} | Total Time: %{time_total}s\\n' http://127.0.0.1:80/web/login"
    _, stdout, _ = ssh.exec_command(cmd_curl)
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    stabilize_server()
