import paramiko

def read_vehiculo_model():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "cat /opt/synergia/addons_fundetaxcol/fundetaxcol/models/vehiculo_model.py"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- VEHICULO_MODEL.PY ---")
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_vehiculo_model()
