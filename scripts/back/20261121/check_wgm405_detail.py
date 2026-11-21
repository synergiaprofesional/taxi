import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_sql(query):
    # Use python on remote or clean command
    cmd = f"sudo -u postgres psql -d fundetaxcol -c \"{query}\""
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.read().decode('utf-8', errors='ignore')

print("=== 1. TURNOS HISTORICOS DEL VEHICULO WGM405 (ID 4454) ===")
print(run_sql("SELECT id, name, vehiculo_id, conductor_id, bahia_id, sesion_bahia_id, state, create_date FROM fundetaxcol_turno WHERE vehiculo_id = 4454 ORDER BY id DESC LIMIT 10;"))

print("=== 2. PAGOS HISTORICOS DEL VEHICULO WGM405 (ID 4454) ===")
print(run_sql("SELECT id, consecutivo, vehiculo_id, conductor_id, bahia_id, sesion_bahia_id, valor, create_date FROM fundetaxcol_pago WHERE vehiculo_id = 4454 ORDER BY id DESC LIMIT 10;"))

print("=== 3. ULTIMAS 10 SESIONES DE CUALQUIER ESTADO ===")
print(run_sql("SELECT id, name, state, user_id, bahia_id, fecha_apertura, fecha_cierre FROM fundetaxcol_sesion_bahia ORDER BY id DESC LIMIT 10;"))

print("=== 4. ULTIMOS 10 TURNOS EN GENERAL ===")
print(run_sql("SELECT id, name, vehiculo_id, conductor_id, bahia_id, sesion_bahia_id, state, create_date FROM fundetaxcol_turno ORDER BY id DESC LIMIT 10;"))

ssh.close()
