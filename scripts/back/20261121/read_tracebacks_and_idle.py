import paramiko

def read_tracebacks():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "journalctl -u odoo_80.service --since '2 hours ago' -n 200 --no-pager | grep -C 8 'Exception during JSON request handling'"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    # Also let's inspect the two idle in transaction queries in postgres
    cmd2 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT pid, query_start, state, query FROM pg_stat_activity WHERE pid IN (10456, 10457);'"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- 52 DAYS OLD TRANSACTIONS ---")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_tracebacks()
