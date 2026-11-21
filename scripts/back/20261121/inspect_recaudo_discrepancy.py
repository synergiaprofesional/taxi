import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_query(title, sql):
    print(f"\n=== {title} ===")
    cmd = f'sudo -u postgres psql -d fundetaxcol -c "{sql}"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))
    err = stderr.read().decode('utf-8')
    if err:
        print("ERR:", err)

run_query("PAGOS HOY (fundetaxcol_pago)", 
          "SELECT id, name, fecha, valor, vehiculo_id, state FROM fundetaxcol_pago WHERE fecha >= '2026-10-18' ORDER BY id DESC;")

run_query("SUMA TOTAL PAGOS HOY", 
          "SELECT count(*), sum(valor) FROM fundetaxcol_pago WHERE fecha >= '2026-10-18';")

run_query("TURNOS HOY Y SU VALOR_TOTAL", 
          "SELECT id, numero, fecha, state, vehiculo_id, valor_total, bahia_id FROM fundetaxcol_turno WHERE fecha >= '2026-10-18' ORDER BY id ASC;")

run_query("SUMA VALOR_TOTAL DE TURNOS HOY POR ESTADO", 
          "SELECT state, count(*), sum(valor_total) FROM fundetaxcol_turno WHERE fecha >= '2026-10-18' GROUP BY state;")

run_query("SESIONES DE BAHIA HOY", 
          "SELECT table_name FROM information_schema.tables WHERE table_name LIKE '%bahia%' OR table_name LIKE '%sesion%';")

ssh.close()
