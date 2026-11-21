import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_sql(query):
    # Pass SQL via stdin or cd /tmp first
    cmd = f"""cd /tmp && sudo -u postgres psql -d fundetaxcol -c "{query}" """
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='ignore')
    return out

print("=== 1. USUARIOS CON SOTANO O CARIBE ===")
print(run_sql("SELECT id, login, name, active FROM res_users WHERE login ILIKE '%sotano%' OR login ILIKE '%caribe%' OR name ILIKE '%sotano%' OR name ILIKE '%caribe%';"))

print("=== 2. TODAS LAS SESIONES IN_PROGRESS ===")
print(run_sql("SELECT s.id, s.name, s.state, s.user_id, u.login, s.bahia_id, s.fecha_apertura FROM fundetaxcol_sesion_bahia s JOIN res_users u ON s.user_id = u.id WHERE s.state = 'in_progress' ORDER BY s.id DESC;"))

print("=== 3. VEHICULO WGM405 O 405 ===")
print(run_sql("SELECT id, name, active FROM fundetaxcol_vehiculo WHERE name ILIKE '%405%';"))

print("=== 4. TURNOS CREADOS HOY 25 DE OCTUBRE ===")
print(run_sql("SELECT id, name, vehiculo_id, conductor_id, bahia_id, sesion_bahia_id, state, create_date FROM fundetaxcol_turno WHERE create_date >= '2026-10-25 00:00:00' ORDER BY id DESC LIMIT 20;"))

print("=== 5. ULTIMOS 10 PAGOS DE HOY 25 DE OCTUBRE ===")
print(run_sql("SELECT id, consecutivo, vehiculo_id, conductor_id, bahia_id, sesion_bahia_id, valor, create_date FROM fundetaxcol_pago WHERE create_date >= '2026-10-25 00:00:00' ORDER BY id DESC LIMIT 10;"))

ssh.close()
