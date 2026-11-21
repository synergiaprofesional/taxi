import paramiko

def check_server_full_status():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

    print("=== 1. CARGA DE CPU Y SISTEMA (UPTIME & TOP LIVE) ===")
    cmd_top = "top -b -n 2 -d 1 | tail -n 20"
    _, stdout, _ = ssh.exec_command(cmd_top)
    print(stdout.read().decode('utf-8'))

    print("=== 2. MEMORIA DEL SISTEMA ===")
    cmd_mem = "free -h"
    _, stdout, _ = ssh.exec_command(cmd_mem)
    print(stdout.read().decode('utf-8'))

    print("=== 3. CONSULTAS ACTIVAS EN POSTGRESQL ===")
    sql_act = """
    SELECT pid, 
           age(clock_timestamp(), query_start) as duration, 
           state, 
           substring(query from 1 for 120) as query_snippet
    FROM pg_stat_activity 
    WHERE state != 'idle' 
      AND pid != pg_backend_pid();
    """
    _, stdout, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql_act}\"")
    print(stdout.read().decode('utf-8'))

    print("=== 4. ÚLTIMOS LOGS DE ODOO (ÚLTIMOS 3 MINUTOS) ===")
    cmd_log = "journalctl -u odoo_80.service --since '3 minutes ago' --no-pager | tail -n 25"
    _, stdout, _ = ssh.exec_command(cmd_log)
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_server_full_status()
