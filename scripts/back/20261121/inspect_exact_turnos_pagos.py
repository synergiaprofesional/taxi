import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_query(title, sql):
    print(f"\n==================================================")
    print(f"=== {title} ===")
    print(f"==================================================")
    cmd = f'sudo -u postgres psql -d fundetaxcol -c "{sql}"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

run_query("TURNOS HOY (fundetaxcol_turno)", 
          "SELECT id, name, fecha_asignacion, fecha_despacho, state, vehiculo_id, conductor_id, valor, bahia_id FROM fundetaxcol_turno WHERE fecha_asignacion >= '2026-10-18' ORDER BY id ASC;")

run_query("SUMA VALOR TURNOS DESPACHADOS HOY", 
          "SELECT count(*), sum(valor) FROM fundetaxcol_turno WHERE fecha_asignacion >= '2026-10-18' AND state = 'despachado';")

run_query("SUMA VALOR DE TODOS LOS TURNOS HOY", 
          "SELECT state, count(*), sum(valor) FROM fundetaxcol_turno WHERE fecha_asignacion >= '2026-10-18' GROUP BY state;")

run_query("PAGOS HOY (fundetaxcol_pago) DETALLADO", 
          "SELECT id, consecutivo, fecha, valor, vehiculo_id, conductor_id, bahia_id, enturnar FROM fundetaxcol_pago WHERE fecha >= '2026-10-18' ORDER BY id ASC;")

ssh.close()
