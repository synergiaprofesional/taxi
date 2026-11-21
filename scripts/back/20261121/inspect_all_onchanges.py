import paramiko

def inspect_all_onchanges():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "grep -n -C 5 '@api.onchange' /opt/synergia/addons_fundetaxcol/fundetaxcol/models/turno_model.py"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- ONCHANGES EN TURNO_MODEL.PY ---")
    print(stdout.read().decode('utf-8'))

    cmd2 = "grep -n -C 5 '@api.depends' /opt/synergia/addons_fundetaxcol/fundetaxcol/models/turno_model.py"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- DEPENDS EN TURNO_MODEL.PY ---")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    inspect_all_onchanges()
