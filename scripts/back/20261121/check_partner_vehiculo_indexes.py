import paramiko

def check_res_partner_indexes():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    sql = "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'res_partner';"
    cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql}\""
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- ÍNDICES DE RES_PARTNER ---")
    print(stdout.read().decode('utf-8'))

    # Ver también índices en fundetaxcol_vehiculo
    sql2 = "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'fundetaxcol_vehiculo';"
    cmd2 = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql2}\""
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- ÍNDICES DE FUNDETAXCOL_VEHICULO ---")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_res_partner_indexes()
