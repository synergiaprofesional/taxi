import paramiko

def inspect_vehiculo_load_queries():
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
        
        # 1. Medir lectura de vehiculo WGN772 (ID 4066)
        cr_query_count = [0]
        orig_execute = cr.execute
        def count_execute(*args, **kwargs):
            cr_query_count[0] += 1
            return orig_execute(*args, **kwargs)
        cr.execute = count_execute

        t0 = time.time()
        v = env['fundetaxcol.vehiculo'].browse(4066)
        name = v.name
        prop = v.propietario_id.name
        conds = [x.conductor_id.name for x in v.conductor_ids]
        ing = v.ingreso
        total_pagos = len(v.pago_ids)
        total_turnos = len(v.turno_ids)
        t1 = time.time()

        print(f"Lectura completa de Vehiculo {name}:")
        print(f"  Propietario: {prop}")
        print(f"  Conductores en pestaña: {conds}")
        print(f"  Ingresos mes calculados: {ing}")
        print(f"  Total Pagos historicos vinculados: {total_pagos}")
        print(f"  Total Despachos/Turnos vinculados: {total_turnos}")
        print(f"  Tiempo total: {round(t1 - t0, 4)} s | Consultas SQL ejecutadas: {cr_query_count[0]}")
'''
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/bench_vehiculo_queries.py', 'w') as f:
        f.write(remote_code)
    sftp.close()

    _, stdout, stderr = ssh.exec_command('PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/bench_vehiculo_queries.py')
    print("STDOUT:")
    print(stdout.read().decode('utf-8'))
    print("STDERR:")
    print(stderr.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    inspect_vehiculo_load_queries()
