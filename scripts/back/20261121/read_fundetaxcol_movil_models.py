import paramiko

def read_movil_models():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    # Let's inspect the models around 440-540
    cmd = "sed -n '445,535p' /opt/synergia/addons_fundetaxcol/fundetaxcol_movil/models/models.py"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- LINES 445-535 ---")
    print(stdout.read().decode('utf-8'))

    # Let's inspect 310-350
    cmd2 = "sed -n '310,350p' /opt/synergia/addons_fundetaxcol/fundetaxcol_movil/models/models.py"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- LINES 310-350 ---")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_movil_models()
