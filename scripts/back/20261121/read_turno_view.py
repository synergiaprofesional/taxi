import paramiko

def read_turno_view():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "grep -rn -C 10 'model=\"fundetaxcol.turno\"' /opt/synergia/addons_fundetaxcol/"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    # También ver turno_view.xml
    cmd2 = "cat /opt/synergia/addons_fundetaxcol/fundetaxcol/views/turno_view.xml"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- TURNO_VIEW.XML ---")
    print(stdout2.read().decode('utf-8')[:2500])

    ssh.close()

if __name__ == '__main__':
    read_turno_view()
