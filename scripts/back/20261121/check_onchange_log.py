import paramiko

def check_onchange_requests():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "journalctl -u odoo_80.service --since '15 minutes ago' | grep -E 'onchange|call_kw' | tail -n 30"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- PETICIONES RECIENTES A CALL_KW / ONCHANGE ---")
    print(stdout.read().decode('utf-8'))

    # También ver si el log de odoo tiene mensajes con tiempo de ejecución
    cmd2 = "journalctl -u odoo_80.service --since '15 minutes ago' | grep -E 'werkzeug.*(POST|GET)' | tail -n 30"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- ÚLTIMOS REQUESTS WERKZEUG ---")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_onchange_requests()
