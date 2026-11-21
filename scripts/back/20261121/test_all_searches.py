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
        
        # 1. Test search_read on vehiculo (like tree view search)
        print("=== TEST 1: search_read en fundetaxcol.vehiculo ===")
        t0 = time.time()
        fields_tree = ['name', 'propietario_id', 'marca_vehiculo_id', 'tipo', 'tipo_combustible', 'modelo', 'cilindraje', 'ingreso']
        res = env['fundetaxcol.vehiculo'].search_read([('name', 'ilike', 'WGM776')], fields_tree)
        t1 = time.time()
        print(f"search_read('WGM776'): {round((t1-t0)*1000, 2)} ms | rows: {len(res)}")
        
        # 2. Test search_read general (sin filtro, limit 80 como abre la lista)
        t0 = time.time()
        res_all = env['fundetaxcol.vehiculo'].search_read([], fields_tree, limit=80)
        t1 = time.time()
        print(f"search_read(general limit 80): {round((t1-t0)*1000, 2)} ms | rows: {len(res_all)}")
        
        # 3. Test onchange en turno
        print("=== TEST 2: onchange en fundetaxcol.turno ===")
        vehiculo = env['fundetaxcol.vehiculo'].search([('name', '=ilike', 'WGM776')], limit=1)
        turno = env['fundetaxcol.turno'].new({'vehiculo_id': vehiculo.id})
        t0 = time.time()
        turno._onchange_vehiculo_id()
        t1 = time.time()
        print(f"_onchange_vehiculo_id(): {round((t1-t0)*1000, 2)} ms | conductor asignado: {turno.conductor_id.name}")
        
        # 4. Test name_search on conductor
        print("=== TEST 3: name_search en res.partner (conductores) ===")
        t0 = time.time()
        conds = env['res.partner'].name_search(name='JAIRO', args=[('conductor', '=', True)], limit=7)
        t1 = time.time()
        print(f"name_search('JAIRO'): {round((t1-t0)*1000, 2)} ms | {conds}")
'''

sftp = ssh.open_sftp()
with sftp.file('/tmp/test_all_search_ops.py', 'w') as f:
    f.write(remote_code)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/test_all_search_ops.py")
print("STDOUT:")
print(stdout.read().decode('utf-8'))
print("STDERR:")
print(stderr.read().decode('utf-8'))

ssh.close()
