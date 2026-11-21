import paramiko

def read_odoo_turno_create2():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "sed -n '261,350p' /opt/synergia/addons_fundetaxcol/fundetaxcol/models/turno_model.py"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_odoo_turno_create2()
