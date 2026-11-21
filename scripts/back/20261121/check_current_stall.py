import paramiko

def check_odoo_queries_now():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    print("=== CONSULTAS ACTIVAS EN POSTGRESQL ===")
    sql = """
    SELECT pid, 
           age(clock_timestamp(), query_start) as duration, 
           state, 
           query 
    FROM pg_stat_activity 
    WHERE state != 'idle' 
      AND pid != pg_backend_pid();
    """
    _, stdout, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql}\"")
    print(stdout.read().decode('utf-8'))

    print("=== ÚLTIMOS LOGS DE ODOO DE LOS ÚLTIMOS 2 MINUTOS ===")
    cmd_log = "journalctl -u odoo_80.service --since '2 minutes ago' --no-pager"
    _, stdout2, _ = ssh.exec_command(cmd_log)
    print(stdout2.read().decode('utf-8'))

    print("=== ÍNDICES DE FUNDETAXCOL_VEHICULO_CONDUCTOR ===")
    sql2 = "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'fundetaxcol_vehiculo_conductor';"
    _, stdout3, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql2}\"")
    print(stdout3.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_odoo_queries_now()
