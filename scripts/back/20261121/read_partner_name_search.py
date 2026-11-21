import paramiko

def read_partner_name_search():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "grep -n -A 35 'def name_search' /opt/synergia/odoo-11.0/odoo/addons/base/res/res_partner.py"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- RES_PARTNER NAME_SEARCH ---")
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_partner_name_search()
