import paramiko

def select_all_crons():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "cd /tmp && sudo -u postgres psql -d fundetaxcol -x -c 'SELECT * FROM ir_cron;'"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    select_all_crons()
