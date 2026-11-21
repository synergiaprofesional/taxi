import paramiko

def check_partner_table_indexes():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    sql = "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'fundetaxcol_vehiculo_partner';"
    cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql}\""
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- ÍNDICES DE FUNDETAXCOL_VEHICULO_PARTNER ---")
    print(stdout.read().decode('utf-8'))

    # También ver registros de fundetaxcol_vehiculo_partner para el vehiculo WGM776
    sql2 = """
    SELECT vp.id, vp.sequence, vp.vehiculo_id, v.name as placa, vp.conductor_id, p.name as conductor_name 
    FROM fundetaxcol_vehiculo_partner vp
    LEFT JOIN fundetaxcol_vehiculo v ON v.id = vp.vehiculo_id
    LEFT JOIN res_partner p ON p.id = vp.conductor_id
    WHERE v.name = 'WGM776' OR vp.vehiculo_id = 4406;
    """
    cmd2 = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql2}\""
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- CONDUCTORES ASIGNADOS A WGM776 ---")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_partner_table_indexes()
