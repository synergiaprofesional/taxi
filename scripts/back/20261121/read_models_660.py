import paramiko

def read_lines():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "sed -n '660,685p' /opt/synergia/addons_fundetaxcol/fundetaxcol_movil/models/models.py"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    # Also let's see _get_data of this model
    cmd2 = "sed -n '740,780p' /opt/synergia/addons_fundetaxcol/fundetaxcol_movil/models/models.py"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- _get_data ---")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_lines()
