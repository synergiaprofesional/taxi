import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_sql(query, title):
    print(f"\n=== {title} ===")
    cmd = f'sudo -u postgres psql -d fundetaxcol -c "{query}"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='ignore')
    if out:
        print(out)

run_sql("SELECT * FROM fundetaxcol_turno WHERE id = 991104;", "TURNO 991104 DETALLE COMPLETO")

# Ver turnos creados hoy por bahia_id
run_sql("""
SELECT t.id, t.name, t.state, t.bahia_id, t.fecha_asignacion, t.fecha_despacho, v.name as vehiculo, t.create_uid, u.login, t.create_date 
FROM fundetaxcol_turno t 
LEFT JOIN fundetaxcol_vehiculo v ON t.vehiculo_id = v.id 
LEFT JOIN res_users u ON t.create_uid = u.id 
WHERE t.create_date >= '2026-10-25 14:00:00' 
ORDER BY t.id DESC;
""", "TODOS LOS TURNOS DESPUES DE LAS 9 AM (14:00 UTC)")

ssh.close()
