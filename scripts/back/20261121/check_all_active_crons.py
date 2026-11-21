import paramiko

def check_all_active_crons():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    sql = """
    SELECT c.id, c.cron_name, m.model, c.interval_number, c.interval_type, c.nextcall 
    FROM ir_cron c
    LEFT JOIN ir_model m ON m.id = c.model_id
    WHERE c.active = true
    ORDER BY c.id;
    """
    cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql}\""
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- CRONS ACTIVOS COMPLETOS ---")
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_all_active_crons()
