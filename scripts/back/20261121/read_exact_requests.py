import paramiko

def read_exact_requests():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "journalctl -u odoo_80.service --since '09:30:00' --until '09:50:00' | grep -v 'longpolling' | grep -E 'werkzeug|Traceback|ERROR|WARNING' | tail -n 40"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- REQUESTS ENTRE 09:30 Y 09:50 ---")
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_exact_requests()
