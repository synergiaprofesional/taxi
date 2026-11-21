import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_query(title, sql):
    print(f"\n=== {title} ===")
    cmd = f'sudo -u postgres psql -d fundetaxcol -c "{sql}"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

run_query("TODOS LOS PAGOS DE HOY", 
          "SELECT id, name, fecha, valor, vehiculo_id, bahia_id, sesion_id FROM fundetaxcol_pago WHERE fecha >= '2026-10-18' ORDER BY id DESC;")

run_query("COLUMNAS DE FUNDETAXCOL_TURNO", 
          "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'fundetaxcol_turno' ORDER BY ordinal_position;")

run_query("COLUMNAS DE FUNDETAXCOL_PAGO", 
          "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'fundetaxcol_pago' ORDER BY ordinal_position;")

ssh.close()
