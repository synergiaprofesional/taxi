import paramiko

def check_browser_requests():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    print("=== ÚLTIMOS LOGS DE WERKZEUG EN ODOO ===")
    cmd = "journalctl -u odoo_80.service -n 25 --no-pager"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    print("=== TOP PROCESOS EN EL SERVIDOR ===")
    cmd2 = "ps aux | grep odoo-bin | grep -v grep; uptime"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_browser_requests()
