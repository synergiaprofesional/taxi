import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=20)

remote_code = '''import odoo
from odoo import api, SUPERUSER_ID

config_path = '/opt/synergia/odoo-11.0/odoo_80.conf'
odoo.tools.config.parse_config(['-c', config_path])
registry = odoo.registry('fundetaxcol')

with api.Environment.manage():
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        Vehiculo = env['fundetaxcol.vehiculo']
        
        # Test 1: Con dominio de vehiculo_ids vacio (como cuando no hay sesion abierta)
        res_vacio = Vehiculo.name_search(name='WGM776', args=[('id', 'in', [])], operator='ilike', limit=7)
        print("name_search con [('id','in',[])]:", res_vacio)
        
        # Test 2: Sin restriccion de vehiculo_ids (directo a catalogo de vehiculos)
        res_libre = Vehiculo.name_search(name='WGM776', args=[], operator='ilike', limit=7)
        print("name_search sin restriccion:", res_libre)
'''

sftp = ssh.open_sftp()
with sftp.file('/tmp/test_veh_domain.py', 'w') as f:
    f.write(remote_code)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/test_veh_domain.py")
print("STDOUT:")
print(stdout.read().decode('utf-8'))

ssh.close()
