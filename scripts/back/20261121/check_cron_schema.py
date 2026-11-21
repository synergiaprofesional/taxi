import paramiko

def check_ir_cron_cols():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "cd /tmp && sudo -u postgres psql -d fundetaxcol -c 'SELECT column_name, data_type FROM information_schema.columns WHERE table_name = \x27ir_cron\x27;'"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    # También ver cuántos registros hay en ir_cron
    cmd2 = "cd /tmp && sudo -u postgres psql -d fundetaxcol -c 'SELECT count(*), count(*) filter (where active) as active_count FROM ir_cron;'"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_ir_cron_cols()
