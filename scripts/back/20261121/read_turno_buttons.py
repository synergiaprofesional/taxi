import paramiko

def read_turno_buttons():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "grep -n -A 40 'def btn_guardar_turno' /opt/synergia/addons_fundetaxcol/fundetaxcol/models/turno_model.py"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- BTN_GUARDAR_TURNO ---")
    print(stdout.read().decode('utf-8'))

    # También ver create y write
    cmd2 = "sed -n '288,340p' /opt/synergia/addons_fundetaxcol/fundetaxcol/models/turno_model.py"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- SET_SEQUENCE Y CREATE ---")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_turno_buttons()
