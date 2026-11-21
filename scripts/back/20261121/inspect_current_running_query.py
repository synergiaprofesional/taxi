import paramiko

def inspect_current_query_and_onchange():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    print("=== CONSULTA QUE ESTÁ CORRIENDO EN ESTE INSTANTE EN POSTGRESQL ===")
    sql_running = """
    SELECT pid, 
           age(clock_timestamp(), query_start) as duration, 
           state, 
           query 
    FROM pg_stat_activity 
    WHERE state != 'idle' 
      AND pid != pg_backend_pid();
    """
    _, stdout, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql_running}\"")
    print(stdout.read().decode('utf-8'))

    print("=== CÓDIGO DE ONCHANGE VEHICULO_ID EN FUNDETAXCOL.TURNO ===")
    cmd_grep = "grep -rn -A 25 'onchange.*vehiculo_id' /opt/synergia/addons_fundetaxcol/"
    _, stdout2, _ = ssh.exec_command(cmd_grep)
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    inspect_current_query_and_onchange()
