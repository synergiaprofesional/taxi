import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_query(title, sql):
    print(f"\n=== {title} ===")
    cmd = f'sudo -u postgres psql -d fundetaxcol -c "{sql}"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

run_query("PAGOS POR SESION DE BAHIA HOY", """
    SELECT p.bahia_id, sb.name, COUNT(p.id) as cant, SUM(p.valor) as total
    FROM fundetaxcol_pago p
    LEFT JOIN fundetaxcol_sesion_bahia sb ON sb.id = p.bahia_id
    WHERE sb.state = 'opened' OR p.fecha >= '2026-10-18 10:00:00'
    GROUP BY p.bahia_id, sb.name;
""")

run_query("SESIONES DE BAHIA ABIERTAS HOY", """
    SELECT id, name, state, fecha_apertura, fecha_cierre
    FROM fundetaxcol_sesion_bahia
    WHERE state = 'opened' OR create_date >= '2026-10-18 00:00:00';
""")

ssh.close()
