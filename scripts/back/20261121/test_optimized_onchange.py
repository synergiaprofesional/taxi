import paramiko

def test_optimized_onchange():
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
        bahia = env['fundetaxcol.sesion.bahia'].browse(8816) # Garita
        bahia_ids = tuple(bahia.sesion_id.sesion_bahia_ids.ids)

        # 1. Método actual con ORM y loops
        t0 = time.time()
        pagos = env['fundetaxcol.pago'].search([('bahia_id', 'in', bahia_ids)])
        turnos = env['fundetaxcol.turno'].search([('bahia_id', 'in', bahia_ids)])
        vehiculo_ids_orm = env['fundetaxcol.vehiculo']
        for pago in pagos:
            ingreso = len(pago.concepto_ids.filtered(lambda x: x.concepto_id.clasificacion in ('cr_ingreso', 'ingreso')))
            if ingreso != 0:
                vehiculo_ids_orm |= pago.vehiculo_id
        for turno in turnos:
            if turno.state in ('actual', 'espera', 'pausa'):
                vehiculo_ids_orm -= turno.vehiculo_id
        t1 = time.time()
        print("1. Metodo ORM actual tardo:", round(t1 - t0, 4), "s | Vehiculos disponibles:", len(vehiculo_ids_orm))

        # 2. Método SQL optimizado
        t2 = time.time()
        cr.execute("""
            SELECT DISTINCT p.vehiculo_id 
            FROM fundetaxcol_pago p
            JOIN fundetaxcol_pago_concepto pc ON pc.pago_id = p.id
            JOIN fundetaxcol_concepto c ON c.id = pc.concepto_id
            WHERE p.bahia_id IN %s 
              AND c.clasificacion IN ('cr_ingreso', 'ingreso')
              AND p.vehiculo_id IS NOT NULL;
        """, (bahia_ids,))
        pagados = set(r[0] for r in cr.fetchall())

        cr.execute("""
            SELECT DISTINCT vehiculo_id 
            FROM fundetaxcol_turno 
            WHERE bahia_id IN %s 
              AND state IN ('actual', 'espera', 'pausa')
              AND vehiculo_id IS NOT NULL;
        """, (bahia_ids,))
        en_cola = set(r[0] for r in cr.fetchall())

        disponibles_ids = list(pagados - en_cola)
        vehiculo_ids_sql = env['fundetaxcol.vehiculo'].browse(disponibles_ids)
        t3 = time.time()
        print("2. Metodo SQL optimizado tardo:", round(t3 - t2, 4), "s | Vehiculos disponibles:", len(vehiculo_ids_sql))
        print("   Coinciden exactamente los sets?:", set(vehiculo_ids_orm.ids) == set(disponibles_ids))
'''
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/bench_opt_onchange.py', 'w') as f:
        f.write(remote_code)
    sftp.close()

    _, stdout, stderr = ssh.exec_command('PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/bench_opt_onchange.py')
    print("STDOUT:")
    print(stdout.read().decode('utf-8'))
    print("STDERR:")
    print(stderr.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    test_optimized_onchange()
