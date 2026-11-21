import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_query(title, sql):
    print(f"\n=== {title} ===")
    cmd = f'sudo -u postgres psql -d fundetaxcol -c "{sql}"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

run_query("RELACION BAHIA EN PAGO", """
    SELECT
        tc.table_name, kcu.column_name,
        ccu.table_name AS foreign_table_name,
        ccu.column_name AS foreign_column_name
    FROM information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = 'fundetaxcol_pago';
""")

run_query("QUE ES ID 8818 Y 8819", """
    SELECT 'fundetaxcol_bahia' as tbl, id, name FROM fundetaxcol_bahia WHERE id IN (8818, 8819, 8817)
    UNION ALL
    SELECT 'fundetaxcol_sesion_bahia', id, name FROM fundetaxcol_sesion_bahia WHERE id IN (8818, 8819, 8817)
    UNION ALL
    SELECT 'fundetaxcol_sesion', id, name FROM fundetaxcol_sesion WHERE id IN (8818, 8819, 8817);
""")

run_query("HORARIO DE PAGOS HOY EN COLOMBIA", """
    SELECT id, consecutivo, bahia_id, valor, fecha, fecha AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota' as fecha_bogota
    FROM fundetaxcol_pago
    WHERE fecha >= '2026-10-18 10:00:00'
    ORDER BY id ASC;
""")

ssh.close()
