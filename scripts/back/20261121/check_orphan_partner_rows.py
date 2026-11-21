import paramiko

def check_orphan_rows():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    sql = """
    SELECT vp.id, vp.vehiculo_id, vp.conductor_id 
    FROM fundetaxcol_vehiculo_partner vp
    LEFT JOIN fundetaxcol_vehiculo v ON v.id = vp.vehiculo_id
    WHERE v.id IS NULL;
    """
    cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql}\""
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- REGISTROS HUÉRFANOS EN FUNDETAXCOL_VEHICULO_PARTNER ---")
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_orphan_rows()
