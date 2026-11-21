import paramiko

def read_turno_model_vehiculo():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "grep -n -C 20 'vehiculo_id' /opt/synergia/addons_fundetaxcol/fundetaxcol/models/turno_model.py"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_turno_model_vehiculo()
