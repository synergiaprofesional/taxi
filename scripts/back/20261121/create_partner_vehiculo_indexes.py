import paramiko

def add_partner_and_vehiculo_indexes():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

    indexes = [
        ("idx_vehiculo_name", "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_vehiculo_name ON fundetaxcol_vehiculo (name);"),
        ("idx_vehiculo_partner_vehiculo_id", "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_vehiculo_partner_vehiculo_id ON fundetaxcol_vehiculo_partner (vehiculo_id);"),
        ("idx_vehiculo_partner_conductor_id", "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_vehiculo_partner_conductor_id ON fundetaxcol_vehiculo_partner (conductor_id);"),
        ("idx_partner_identificacion", "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_partner_identificacion ON res_partner (identificacion);"),
        ("idx_partner_conductor", "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_partner_conductor ON res_partner (conductor) WHERE conductor = true;")
    ]

    for name, sql in indexes:
        print(f"Creando índice {name}...")
        cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql}\""
        _, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8').strip()
        err = stderr.read().decode('utf-8').strip()
        print(f"Resultado {name}: {out} | {err}")

    ssh.close()

if __name__ == '__main__':
    add_partner_and_vehiculo_indexes()
