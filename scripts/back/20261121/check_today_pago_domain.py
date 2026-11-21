import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_query(title, sql):
    print(f"\n=== {title} ===")
    cmd = f'sudo -u postgres psql -d fundetaxcol -c "{sql}"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

run_query("MIN Y MAX FECHA DE PAGOS HOY", """
    SELECT MIN(fecha) as min_fecha, MAX(fecha) as max_fecha, COUNT(*) as total_pagos, SUM(valor) as total_valor
    FROM fundetaxcol_pago
    WHERE fecha >= '2026-10-18 00:00:00';
""")

run_query("PAGOS POR FECHA HOY (DESDE 05:00 UTC)", """
    SELECT COUNT(*) as total_pagos, SUM(valor) as total_valor
    FROM fundetaxcol_pago
    WHERE fecha >= '2026-10-18 05:00:00';
""")

ssh.close()
