import paramiko

def check_tcp_connections():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    print("=== CONEXIONES TCP AL PUERTO 80 ===")
    cmd = "netstat -tnpa | grep ':80 '"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    print("=== ESTADO DEL PROCESO ODOO ===")
    cmd2 = "ps aux | grep odoo-bin | grep -v grep"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_tcp_connections()
