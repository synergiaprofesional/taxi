import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_query(title, sql):
    print(f"\n=== {title} ===")
    cmd = f'sudo -u postgres psql -d fundetaxcol -c "{sql}"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

run_query("PAGOS POR BAHIA HOY", """
    SELECT p.bahia_id, b.name as bahia_nombre, count(*), sum(p.valor) 
    FROM fundetaxcol_pago p 
    LEFT JOIN fundetaxcol_bahia b ON p.bahia_id = b.id 
    WHERE p.fecha >= '2026-10-18' 
    GROUP BY p.bahia_id, b.name;
""")

run_query("PAGOS POR SESION HOY", """
    SELECT p.sesion_id, count(*), sum(p.valor)
    FROM fundetaxcol_pago p
    WHERE p.fecha >= '2026-10-18'
    GROUP BY p.sesion_id;
""")

run_query("TODOS LOS PAGOS HOY (DETALLE)", """
    SELECT p.id, p.consecutivo, p.bahia_id, b.name as bahia, p.valor, p.fecha
    FROM fundetaxcol_pago p
    LEFT JOIN fundetaxcol_bahia b ON p.bahia_id = b.id
    WHERE p.fecha >= '2026-10-18'
    ORDER BY p.id DESC;
""")

run_query("TURNOS DESPACHADOS HOY EN BAHIA", """
    SELECT b.name as bahia, count(*), sum(t.tarifa_valor)
    FROM fundetaxcol_turno t
    LEFT JOIN fundetaxcol_bahia b ON t.bahia_id = b.id
    WHERE t.fecha >= '2026-10-18'
    GROUP BY b.name;
""")

ssh.close()
