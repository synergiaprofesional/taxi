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
        Vehiculo = env['fundetaxcol.vehiculo']
        
        for q in ['WGM', 'WGM776', '123']:
            t0 = time.time()
            res = Vehiculo.name_search(name=q, args=[], operator='ilike', limit=7)
            t1 = time.time()
            print("name_search('" + str(q) + "'): " + str(round((t1-t0)*1000, 2)) + " ms | results: " + str(res))
'''

sftp = ssh.open_sftp()
with sftp.file('/tmp/test_veh_search.py', 'w') as f:
    f.write(remote_code)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/test_veh_search.py")
print("STDOUT:", stdout.read().decode('utf-8'))
print("STDERR:", stderr.read().decode('utf-8'))

ssh.close()
