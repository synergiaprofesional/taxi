import paramiko

def read_lines():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "sed -n '280,315p' /opt/synergia/addons_fundetaxcol/fundetaxcol_movil/models/models.py"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    # Let's also read 680-720
    cmd2 = "sed -n '680,720p' /opt/synergia/addons_fundetaxcol/fundetaxcol_movil/models/models.py"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- LINES 680-720 ---")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_lines()
