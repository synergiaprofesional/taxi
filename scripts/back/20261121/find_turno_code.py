import paramiko

def find_code():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "grep -rn 'def get_all' /opt/odoo 2>/dev/null"
    _, stdout, _ = ssh.exec_command(cmd)
    print("=== GET_ALL EN ODOO ===")
    print(stdout.read().decode('utf-8'))

    cmd2 = "find /opt -name '*turno*.py' 2>/dev/null"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("=== ARCHIVOS TURNO EN OPT ===")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    find_code()
