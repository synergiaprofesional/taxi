import paramiko

def cat_bahias():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "sudo -u postgres psql -d fundetaxcol -c 'SELECT id, name FROM fundetaxcol_bahia;'"
    _, stdout, _ = ssh.exec_command(cmd)
    print("FUNDETAXCOL_BAHIA:")
    print(stdout.read().decode('utf-8'))

    cmd2 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT id, sesion_id, bahia_id, state FROM fundetaxcol_sesion_bahia WHERE sesion_id = 2940;'"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("SESION 2940 BAHIAS:")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    cat_bahias()
