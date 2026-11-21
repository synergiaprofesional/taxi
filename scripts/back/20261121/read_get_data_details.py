import paramiko

def read_get_data():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "sed -n '780,820p' /opt/synergia/addons_fundetaxcol/fundetaxcol_movil/models/models.py"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_get_data()
