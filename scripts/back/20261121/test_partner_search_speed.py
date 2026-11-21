import paramiko

def test_partner_search():
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
        
        Partner = env['res.partner']
        
        # 1. Búsqueda por nombre sin dominio
        t0 = time.time()
        res1 = Partner.name_search('JAIRO', args=[('conductor', '=', True)], limit=8)
        t1 = time.time()
        print("Busqueda por nombre 'JAIRO' con domain conductor=True:", len(res1), "resultados en", round(t1 - t0, 4), "s")
        for r in res1[:3]:
            print("   ->", r)

        # 2. Búsqueda por cédula / identificación
        t2 = time.time()
        # Tomemos la cédula de un conductor
        cond = Partner.search([('conductor', '=', True), ('identificacion', '!=', False)], limit=1)
        cedula = cond.identificacion if cond else '123456'
        print(f"Probando busqueda de cedula '{cedula}' (Conductor: {cond.name}):")
        
        res2 = Partner.name_search(cedula, args=[('conductor', '=', True)], limit=8)
        t3 = time.time()
        print("   name_search(cedula):", res2, "en", round(t3 - t2, 4), "s")
        
        # 3. ¿Existe name_search con identificacion?
        res3 = Partner.search([('conductor', '=', True), '|', ('name', 'ilike', cedula), ('identificacion', 'ilike', cedula)], limit=8)
        t4 = time.time()
        print("   search(name ilike OR identificacion ilike):", [(p.id, p.name, p.identificacion) for p in res3], "en", round(t4 - t3, 4), "s")
'''
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/bench_partner_search.py', 'w') as f:
        f.write(remote_code)
    sftp.close()

    _, stdout, stderr = ssh.exec_command('PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/bench_partner_search.py')
    print("STDOUT:")
    print(stdout.read().decode('utf-8'))
    print("STDERR:")
    print(stderr.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    test_partner_search()
