import paramiko

def test_onchange_speed():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

    remote_code = '''
import odoo
from odoo import api, SUPERUSER_ID
import time

config_path = '/opt/synergia/odoo-11.0/odoo_80.conf'
odoo.tools.config.parse_config(['-c', config_path])
registry = odoo.registry('fundetaxcol')

with api.Environment.manage():
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # 1. Buscar vehiculo wgm776
        t0 = time.time()
        vehiculo = env['fundetaxcol.vehiculo'].search([('name', '=ilike', 'wgm776%')], limit=1)
        t1 = time.time()
        print("1. Busqueda vehiculo wgm776:", vehiculo.name, "ID:", vehiculo.id, "tardo:", round(t1 - t0, 4), "s")
        
        # 2. Medir _onchange_bahia_id
        t2 = time.time()
        bahia = env['fundetaxcol.sesion.bahia'].browse(8816) # Garita activa
        turno_new = env['fundetaxcol.turno'].new({'bahia_id': bahia.id})
        print("2. Crear new turno en memoria tardo:", round(time.time() - t2, 4), "s")
        
        t3 = time.time()
        turno_new._onchange_bahia_id()
        t4 = time.time()
        print("3. _onchange_bahia_id(): tardo:", round(t4 - t3, 4), "s | vehiculo_ids calculados:", len(turno_new.vehiculo_ids))
        
        # 3. Medir _onchange_vehiculo_id
        t5 = time.time()
        turno_new.vehiculo_id = vehiculo
        turno_new._onchange_vehiculo_id()
        t6 = time.time()
        print("4. _onchange_vehiculo_id(): tardo:", round(t6 - t5, 4), "s | conductor:", (turno_new.conductor_id.name if turno_new.conductor_id else 'None'), "| conductor_ids:", len(turno_new.conductor_ids))

        # 4. Probar la llamada onchange exacta que hace el navegador
        t7 = time.time()
        specs = {
            'vehiculo_id': '1', 
            'conductor_id': '1', 
            'conductor_ids': '1',
            'vehiculo_ids': '1',
            'bahia_id': '1'
        }
        values = {
            'bahia_id': bahia.id,
            'vehiculo_id': vehiculo.id,
            'conductor_id': False,
            'sequence': 212
        }
        res = env['fundetaxcol.turno'].onchange(values, ['vehiculo_id'], specs)
        t8 = time.time()
        print("5. Metodo onchange(['vehiculo_id']) de Odoo tardo:", round(t8 - t7, 4), "s")
        print("   Resultado value keys:", list(res.get('value', {}).keys()))
'''
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/bench_onchange.py', 'w') as f:
        f.write(remote_code)
    sftp.close()

    _, stdout, stderr = ssh.exec_command('PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/bench_onchange.py')
    print("STDOUT:")
    print(stdout.read().decode('utf-8'))
    print("STDERR:")
    print(stderr.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    test_onchange_speed()
