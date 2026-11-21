import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_sql(query):
    # Escape double quotes for bash
    cmd = f"""sudo -u postgres psql -d fundetaxcol -A -F '|' -c "{query}" """
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    return out, err

print("=== 1. BUSCAR VEHICULO WGM405 ===")
out, _ = run_sql("SELECT id, name, placa, numero_interno, partner_id, active FROM fundetaxcol_vehiculo WHERE name ILIKE '%405%' OR placa ILIKE '%405%';")
print(out)

print("\n=== 2. ULTIMOS TURNOS DE VEHICULO 405 (HOY Y AYER) ===")
out, _ = run_sql("""
SELECT t.id, t.name as turno_num, t.state, t.vehiculo_id, v.name as vehiculo, 
       t.bahia_id, b.name as bahia, t.sesion_bahia_id, t.conductor_id, t.create_date, t.write_date
FROM fundetaxcol_turno t
LEFT JOIN fundetaxcol_vehiculo v ON t.vehiculo_id = v.id
LEFT JOIN fundetaxcol_bahia b ON t.bahia_id = b.id
WHERE v.name ILIKE '%405%' OR v.placa ILIKE '%405%'
ORDER BY t.id DESC LIMIT 10;
""")
print(out)

print("\n=== 3. SESIONES ABIERTAS HOY (24 Y 25 DE OCTUBRE) ===")
out, _ = run_sql("""
SELECT s.id, s.name, s.state, s.user_id, u.login, s.bahia_id, b.name as bahia, s.fecha_apertura, s.fecha_cierre
FROM fundetaxcol_sesion_bahia s
LEFT JOIN res_users u ON s.user_id = u.id
LEFT JOIN fundetaxcol_bahia b ON s.bahia_id = b.id
WHERE s.state = 'in_progress' OR s.fecha_apertura >= '2026-10-24 00:00:00'
ORDER BY s.id DESC LIMIT 15;
""")
print(out)

print("\n=== 4. BAHIAS EXISTENTES (ESPECIALMENTE SOTANO / CARIBE PLAZA) ===")
out, _ = run_sql("SELECT id, name, active, tipo FROM fundetaxcol_bahia;")
print(out)

ssh.close()
