import paramiko

def disable_fetchmail():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "cd /tmp && sudo -u postgres psql -d fundetaxcol -c 'UPDATE ir_cron SET active = false WHERE id = 4;'"
    _, stdout, _ = ssh.exec_command(cmd)
    print("Desactivado cron ID 4 (Fetchmail):", stdout.read().decode('utf-8').strip())

    ssh.close()

if __name__ == '__main__':
    disable_fetchmail()
