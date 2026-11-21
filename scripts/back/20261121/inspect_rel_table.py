import paramiko

def inspect_rel_table():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "sudo -u postgres psql -d fundetaxcol -c 'SELECT count(*) FROM fundetaxcol_pago_fundetaxcol_vehiculo_rel;'"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- COUNT REL ---")
    print(stdout.read().decode('utf-8'))

    cmd2 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT * FROM fundetaxcol_pago_fundetaxcol_vehiculo_rel LIMIT 10;'"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- SAMPLE REL ---")
    print(stdout2.read().decode('utf-8'))

    # Let's check how many unique pagos vs unique vehiculos
    cmd3 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT count(distinct fundetaxcol_pago_id) as unique_pagos, count(distinct fundetaxcol_vehiculo_id) as unique_vehiculos FROM fundetaxcol_pago_fundetaxcol_vehiculo_rel;'"
    _, stdout3, _ = ssh.exec_command(cmd3)
    print("--- DISTINCT REL ---")
    print(stdout3.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    inspect_rel_table()
