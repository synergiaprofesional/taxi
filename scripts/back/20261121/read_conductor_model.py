import paramiko

def read_conductor_model():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "cat /opt/synergia/addons_fundetaxcol/fundetaxcol/models/conductor_model.py"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- CONDUCTOR_MODEL.PY ---")
    print(stdout.read().decode('utf-8'))

    # También ver cuántos conductores hay en res_partner
    cmd2 = "cd /tmp && sudo -u postgres psql -d fundetaxcol -c 'SELECT count(*) as total_partners, count(*) filter (where conductor) as total_conductores FROM res_partner;'"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_conductor_model()
