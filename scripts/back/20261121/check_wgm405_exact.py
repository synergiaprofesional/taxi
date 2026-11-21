import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_sql(query, title):
    print(f"\n=== {title} ===")
    cmd = f'sudo -u postgres psql -d fundetaxcol -c "{query}"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if out:
        print(out)
    if err and "could not change directory" not in err:
        print("ERR:", err)

# 1. Turnos de WGM405
run_sql("SELECT id, name, fecha_asignacion, fecha_despacho, bahia_id, state, vehiculo_id, create_uid, create_date FROM fundetaxcol_turno WHERE vehiculo_id = 4454 ORDER BY id DESC LIMIT 10;", "TURNOS WGM405 (ID 4454)")

# 2. Pagos de WGM405
run_sql("SELECT id, consecutivo, fecha, bahia_id, valor, enturnar, create_uid, create_date FROM fundetaxcol_pago WHERE vehiculo_id = 4454 ORDER BY id DESC LIMIT 10;", "PAGOS WGM405 (ID 4454)")

# 3. Ultimos 15 turnos creados hoy (2026-10-25)
run_sql("SELECT t.id, t.name, t.state, t.bahia_id, b.name as bahia, v.name as vehiculo, t.create_uid, u.login, t.create_date FROM fundetaxcol_turno t LEFT JOIN fundetaxcol_bahia b ON t.bahia_id = b.id LEFT JOIN fundetaxcol_vehiculo v ON t.vehiculo_id = v.id LEFT JOIN res_users u ON t.create_uid = u.id WHERE t.create_date >= '2026-10-25 00:00:00' ORDER BY t.id DESC LIMIT 15;", "TURNOS HOY 25 DE OCTUBRE")

# 4. Ultimos 15 pagos creados hoy (2026-10-25)
run_sql("SELECT p.id, p.consecutivo, p.bahia_id, b.name as bahia, v.name as vehiculo, p.valor, p.enturnar, p.create_uid, u.login, p.create_date FROM fundetaxcol_pago p LEFT JOIN fundetaxcol_bahia b ON p.bahia_id = b.id LEFT JOIN fundetaxcol_vehiculo v ON p.vehiculo_id = v.id LEFT JOIN res_users u ON p.create_uid = u.id WHERE p.create_date >= '2026-10-25 00:00:00' ORDER BY p.id DESC LIMIT 15;", "PAGOS HOY 25 DE OCTUBRE")

ssh.close()
