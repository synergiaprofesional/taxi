import paramiko

def check_bays():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "sudo -u postgres psql -d fundetaxcol -c 'SELECT id, name_sec, name, state, sesion_id FROM fundetaxcol_sesion_bahia ORDER BY id DESC LIMIT 10;'"
    _, stdout, _ = ssh.exec_command(cmd)
    print("=== BAHIAS RECIENTES ===")
    print(stdout.read().decode('utf-8'))

    cmd2 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT id, name, state, date_start FROM fundetaxcol_sesion ORDER BY id DESC LIMIT 5;'"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("=== SESIONES RECIENTES ===")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_bays()
