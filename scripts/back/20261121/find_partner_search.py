import paramiko

def find_name_search():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "grep -rn 'def name_search' /opt/synergia/addons_fundetaxcol/"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- DEF NAME_SEARCH EN ADDONS ---")
    print(stdout.read().decode('utf-8'))

    # También ver qué modelos extienden res.partner
    cmd2 = "grep -rn '_inherit.*res.partner' /opt/synergia/addons_fundetaxcol/"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- INHERIT RES.PARTNER EN ADDONS ---")
    print(stdout2.read().decode('utf-8'))

    # Y ver los campos e índices de res_partner en PostgreSQL
    cmd3 = "cd /tmp && sudo -u postgres psql -d fundetaxcol -c 'SELECT indexname, indexdef FROM pg_indexes WHERE tablename = \x27res_partner\x27;'"
    _, stdout3, _ = ssh.exec_command(cmd3)
    print("--- ÍNDICES DE RES_PARTNER ---")
    print(stdout3.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    find_name_search()
