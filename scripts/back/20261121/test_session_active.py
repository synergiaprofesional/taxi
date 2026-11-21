import paramiko

def check_active_session():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "sudo -u postgres psql -d fundetaxcol -c \"SELECT id, name, state FROM fundetaxcol_sesion ORDER BY id DESC LIMIT 5;\""
    _, stdout, stderr = ssh.exec_command(cmd)
    print("ULTIMAS 5 SESIONES:")
    print(stdout.read().decode('utf-8'))
    ssh.close()

if __name__ == '__main__':
    check_active_session()
