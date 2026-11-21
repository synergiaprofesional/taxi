import paramiko

def inspect_cron_2():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    # 1. Ver qué cron es el id=2
    cmd = "sudo -u postgres psql -d fundetaxcol -c 'SELECT id, name, model, function, interval_number, interval_type, numbercall, active, nextcall FROM ir_cron WHERE id=2;'"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- CRON ID 2 ---")
    print(stdout.read().decode('utf-8'))

    # 2. Ver todos los crons activos
    cmd2 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT id, name, model, function, active, nextcall FROM ir_cron WHERE active=true ORDER BY id;'"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- CRONS ACTIVOS ---")
    print(stdout2.read().decode('utf-8'))

    # 3. Ver tamaño de las tablas y bloat en PostgreSQL
    cmd3 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT schemaname, relname, n_dead_tup, n_live_tup, round(n_dead_tup * 100.0 / nullif(n_live_tup + n_dead_tup, 0),2) as dead_pct, last_autovacuum, last_autoanalyze FROM pg_stat_user_tables WHERE n_dead_tup > 1000 ORDER BY n_dead_tup DESC;'"
    _, stdout3, _ = ssh.exec_command(cmd3)
    print("--- DEAD TUPLES / BLOAT (TABLAS CON MAS DE 1000 DEAD TUPLES) ---")
    print(stdout3.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    inspect_cron_2()
