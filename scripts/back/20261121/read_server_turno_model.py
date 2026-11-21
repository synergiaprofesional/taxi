import paramiko

def read_odoo_turno_model():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    # Let's inspect get_all or fields in turno_model.py
    cmd = "cat /opt/synergia/addons_fundetaxcol/fundetaxcol/models/turno_model.py"
    _, stdout, _ = ssh.exec_command(cmd)
    content = stdout.read().decode('utf-8')
    print("Length of file:", len(content))
    lines = content.split('\n')
    for i, line in enumerate(lines[:60]):
        print(f"{i+1}: {line}")

    ssh.close()

if __name__ == '__main__':
    read_odoo_turno_model()
