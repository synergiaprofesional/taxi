import paramiko

def read_full_turno_views():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "cat /opt/synergia/addons_fundetaxcol/fundetaxcol/views/turno_view.xml"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- TURNO_VIEW.XML COMPLETO ---")
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_full_turno_views()
