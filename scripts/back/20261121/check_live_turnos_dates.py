import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

script = """
import odoo
from odoo import api
import odoo.tools.config as config
config.parse_config(['-c', '/opt/synergia/odoo-11.0/odoo_80.conf'])
registry = odoo.registry('fundetaxcol')
with odoo.api.Environment.manage():
    with registry.cursor() as cr:
        env = api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        # Columnas de fundetaxcol_turno
        cr.execute('''
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'fundetaxcol_turno'
            AND (column_name LIKE '%date%' OR column_name LIKE '%fecha%' OR column_name LIKE '%time%');
        ''')
        cols = cr.fetchall()
        print("COLUMNAS DE FECHA/HORA EN fundetaxcol_turno:", cols)
        
        # Consultar los turnos de hoy
        cr.execute('''
            SELECT t.id, t.name, t.sequence, v.name as placa, t.create_date, t.write_date, t.state
            FROM fundetaxcol_turno t
            LEFT JOIN fundetaxcol_vehiculo v ON t.vehiculo_id = v.id
            WHERE t.create_date >= CURRENT_DATE - INTERVAL '1 day'
            ORDER BY t.id DESC
            LIMIT 10;
        ''')
        rows = cr.fetchall()
        print("\\nSQL DIRECT ROWS:")
        for r in rows:
            print(f"ID: {r[0]} | Name: {r[1]} | Seq: {r[2]} | Placa: {r[3]} | create_date: {r[4]} | write_date: {r[5]} | state: {r[6]}")
            
        print("\\nODOO ORM TurnoMovil._get_data() or get_all:")
        bays = env['fundetaxcol.sesion.bahia'].search([('state', '=', 'progreso')]).ids
        turnos_orm = env['fundetaxcol.turno'].get_all(bahia_ids=bays)
        for t in turnos_orm[:5]:
            print(f"ID: {t.get('id')} | Name: {t.get('name')} | Placa: {t.get('placa')} | Dict keys: {list(t.keys())}")
            print(f"   -> 'fecha': {t.get('fecha')} | 'create_date': {t.get('create_date')}")
"""

sftp = ssh.open_sftp()
with sftp.file('/tmp/check_turnos_dates.py', 'w') as f:
    f.write(script)
sftp.close()

cmd = "PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/check_turnos_dates.py"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("STDOUT:\n", stdout.read().decode('utf-8'))
err = stderr.read().decode('utf-8')
if "Traceback" in err:
    print("STDERR:\n", err)

ssh.close()
