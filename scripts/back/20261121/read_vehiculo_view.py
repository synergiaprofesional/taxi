import paramiko

def read_vehiculo_view():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "cat /opt/synergia/addons_fundetaxcol/fundetaxcol/views/vehiculo_view.xml"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- VEHICULO_VIEW.XML ---")
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_vehiculo_view()
