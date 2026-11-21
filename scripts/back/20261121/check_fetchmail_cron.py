import paramiko

def check_fetchmail_cron():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    sql = """
    SELECT id, name, model, function, interval_number, interval_type, active, nextcall 
    FROM ir_cron 
    WHERE model LIKE '%mail%' OR name LIKE '%mail%' OR name LIKE '%Mail%' OR name LIKE '%Correo%';
    """
    cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql}\""
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- CRONS DE CORREO / FETCHMAIL ---")
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_fetchmail_cron()
