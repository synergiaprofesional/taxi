import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=20)

remote_code = '''import odoo
from odoo import api, SUPERUSER_ID
import time

config_path = '/opt/synergia/odoo-11.0/odoo_80.conf'
odoo.tools.config.parse_config(['-c', config_path])
registry = odoo.registry('fundetaxcol')

with api.Environment.manage():
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        bahia = env['fundetaxcol.sesion.bahia'].search([], limit=1, order='id desc')
        print(f"Bahia ID: {bahia.id} - {bahia.bahia_id.name}")
        
        turno = env['fundetaxcol.turno'].new({'bahia_id': bahia.id})
        t0 = time.time()
        turno._onchange_bahia_id()
        t1 = time.time()
        print(f"TIEMPO _onchange_bahia_id(): {round(t1 - t0, 4)} s")
        print(f"Total vehiculo_ids permitidos: {len(turno.vehiculo_ids)}")
'''

sftp = ssh.open_sftp()
with sftp.file('/tmp/test_bahia_onchange.py', 'w') as f:
    f.write(remote_code)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/test_bahia_onchange.py")
print("STDOUT:")
print(stdout.read().decode('utf-8'))
print("STDERR:")
print(stderr.read().decode('utf-8'))

ssh.close()
