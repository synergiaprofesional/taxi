import paramiko

def inspect_records():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "sudo -u postgres psql -d fundetaxcol -c 'SELECT column_name FROM information_schema.columns WHERE table_name = \"fundetaxcol_sesion_bahia\";'"
    _, stdout, _ = ssh.exec_command(cmd)
    print("=== COLUMNAS ===")
    print(stdout.read().decode('utf-8'))

    cmd2 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT id, sesion_id, bahia_id, state FROM fundetaxcol_sesion_bahia ORDER BY id DESC LIMIT 5;'"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("=== ULTIMAS 5 FILAS ===")
    print(stdout2.read().decode('utf-8'))

    cmd3 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT id, name, codigo FROM fundetaxcol_bahia;'"
    _, stdout3, _ = ssh.exec_command(cmd3)
    print("=== CATALOGO BAHIAS ===")
    print(stdout3.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    inspect_records()
