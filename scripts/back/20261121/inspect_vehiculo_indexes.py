import paramiko

def inspect_vehiculo_indexes():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    print("=== ÍNDICES DE FUNDETAXCOL_VEHICULO ===")
    sql = "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'fundetaxcol_vehiculo';"
    _, stdout, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql}\"")
    print(stdout.read().decode('utf-8'))

    print("=== ÍNDICES DE FUNDETAXCOL_BAHIA ===")
    sql2 = "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'fundetaxcol_bahia';"
    _, stdout2, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql2}\"")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    inspect_vehiculo_indexes()
