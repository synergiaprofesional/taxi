import paramiko

def find_tables():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "sudo -u postgres psql -d fundetaxcol -c \"SELECT table_name FROM information_schema.tables WHERE table_name LIKE '%bahia%' OR table_name LIKE '%sesion%';\""
    _, stdout, _ = ssh.exec_command(cmd)
    print("=== TABLAS ENCONTRADAS ===")
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    find_tables()
