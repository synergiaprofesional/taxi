import paramiko

def check_db():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd1 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT id, name, sequence, state, vehiculo_id, conductor_id, bahia_id, tarifa_id, total, anonimo, placa_anonima FROM fundetaxcol_turno ORDER BY id DESC LIMIT 5;'"
    _, stdout1, _ = ssh.exec_command(cmd1)
    print("=== TURNOS RECIENTES ===")
    print(stdout1.read().decode('utf-8'))

    cmd2 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT column_name, data_type FROM information_schema.columns WHERE table_name = \"fundetaxcol_vehiculo\";'"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("=== COLUMNAS VEHICULO ===")
    print(stdout2.read().decode('utf-8'))

    cmd3 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT id, name FROM fundetaxcol_vehiculo LIMIT 5;'"
    _, stdout3, _ = ssh.exec_command(cmd3)
    print("=== VEHICULOS ===")
    print(stdout3.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_db()
