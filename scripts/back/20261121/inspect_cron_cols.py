import paramiko

def inspect_cron_table():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "sudo -u postgres psql -d fundetaxcol -c 'SELECT column_name, data_type FROM information_schema.columns WHERE table_name = \"ir_cron\";'"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- COLUMNS IR_CRON ---")
    print(stdout.read().decode('utf-8'))

    # Let's inspect id=2 with SELECT *
    cmd2 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT * FROM ir_cron WHERE id=2;'"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- SELECT * FROM IR_CRON WHERE ID=2 ---")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    inspect_cron_table()
