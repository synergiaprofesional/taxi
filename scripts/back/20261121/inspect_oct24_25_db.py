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
    if err:
        print("ERR:", err)

# 1. Sesiones recientes
run_sql("SELECT id, name, fecha, state, user_id FROM fundetaxcol_sesion ORDER BY id DESC LIMIT 5;", "SESIONES RECIENTES")

# 2. Sesiones bahia recientes
run_sql("SELECT id, name, bahia_id, sesion_id, state FROM fundetaxcol_sesion_bahia ORDER BY id DESC LIMIT 10;", "SESIONES BAHIA RECIENTES")

# 3. Pagos recientes (fecha >= 2026-10-24)
run_sql("SELECT id, consecutivo, fecha, bahia_id, valor, enturnar FROM fundetaxcol_pago WHERE fecha >= '2026-10-24 00:00:00' ORDER BY id DESC LIMIT 15;", "PAGOS 24 Y 25 OCTUBRE")

# 4. Turnos recientes (fecha >= 2026-10-24)
run_sql("SELECT id, name, fecha, bahia_id, state, vehiculo_id FROM fundetaxcol_turno WHERE fecha >= '2026-10-24 00:00:00' ORDER BY id DESC LIMIT 15;", "TURNOS 24 Y 25 OCTUBRE")

# 5. Definicion de get_all en fundetaxcol.pago
print("\n=== DEFINICION DE get_all EN fundetaxcol.pago EN ODOO ===")
cmd = "grep -rn 'def get_all' /opt/synergia/addons/ -A 35"
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode('utf-8', errors='ignore')[:3000])

ssh.close()
