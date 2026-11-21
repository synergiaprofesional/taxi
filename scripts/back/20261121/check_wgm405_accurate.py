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

# 1. Sesiones bahia abiertas / recientes
run_sql("SELECT id, name, bahia_id, sesion_id, state FROM fundetaxcol_sesion_bahia ORDER BY id DESC LIMIT 10;", "SESIONES BAHIA RECIENTES")

# 2. Turnos de WGM405
run_sql("SELECT id, name, fecha, bahia_id, sesion_id, state, vehiculo_id FROM fundetaxcol_turno WHERE vehiculo_id = 4454 ORDER BY id DESC LIMIT 10;", "TURNOS WGM405")

# 3. Pagos de WGM405
run_sql("SELECT id, consecutivo, fecha, bahia_id, sesion_id, valor, enturnar FROM fundetaxcol_pago WHERE vehiculo_id = 4454 ORDER BY id DESC LIMIT 10;", "PAGOS WGM405")

# 4. Turnos mas recientes de hoy en general
run_sql("SELECT id, name, fecha, bahia_id, sesion_id, state, vehiculo_id FROM fundetaxcol_turno ORDER BY id DESC LIMIT 15;", "ULTIMOS TURNOS GENERALES")

# 5. Pagos mas recientes de hoy en general
run_sql("SELECT id, consecutivo, fecha, bahia_id, sesion_id, valor, enturnar FROM fundetaxcol_pago ORDER BY id DESC LIMIT 10;", "ULTIMOS PAGOS GENERALES")

ssh.close()
