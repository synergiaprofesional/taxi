import paramiko

def read_bahia_methods():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "grep -n -A 30 'def update_turno_actual' /opt/synergia/addons_fundetaxcol/fundetaxcol/models/*"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- UPDATE_TURNO_ACTUAL ---")
    print(stdout.read().decode('utf-8'))

    cmd2 = "grep -n -A 30 'def update_numero_turno' /opt/synergia/addons_fundetaxcol/fundetaxcol/models/*"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- UPDATE_NUMERO_TURNO ---")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_bahia_methods()
