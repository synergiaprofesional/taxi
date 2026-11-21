import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

script = """
import inspect
import odoo
from odoo import api
import odoo.tools.config as config
config.parse_config(['-c', '/opt/synergia/odoo-11.0/odoo_80.conf'])
registry = odoo.registry('fundetaxcol')
with odoo.api.Environment.manage():
    with registry.cursor() as cr:
        env = api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        # Consultar pagos de hoy
        cr.execute('''
            SELECT id, consecutivo, fecha, create_date, valor
            FROM fundetaxcol_pago
            WHERE create_date >= CURRENT_DATE - INTERVAL '1 day'
            ORDER BY id DESC
            LIMIT 5;
        ''')
        rows = cr.fetchall()
        print("SQL DIRECT fundetaxcol_pago:")
        for r in rows:
            print(f"ID: {r[0]} | Consecutivo: {r[1]} | fecha: {r[2]} | create_date: {r[3]} | valor: {r[4]}")
            
        pago_cls = type(env['fundetaxcol.pago'])
        for name in ['get_data', '_get_data', 'get_all']:
            if hasattr(pago_cls, name):
                print(f"=== fundetaxcol.pago {name} ===")
                try:
                    print(inspect.getsource(getattr(pago_cls, name)))
                except Exception as e:
                    print(e)
"""

sftp = ssh.open_sftp()
with sftp.file('/tmp/check_pago_dates.py', 'w') as f:
    f.write(script)
sftp.close()

cmd = "PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/check_pago_dates.py"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("STDOUT:\n", stdout.read().decode('utf-8'))
err = stderr.read().decode('utf-8')
if "Traceback" in err:
    print("STDERR:\n", err)

ssh.close()

