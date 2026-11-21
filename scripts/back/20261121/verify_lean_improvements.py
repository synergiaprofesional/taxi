import paramiko
import time

def verify_improvements():
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
        
        # 1. Carga de vista form de fundetaxcol.vehiculo (WGN772)
        t0 = time.time()
        v = env['fundetaxcol.vehiculo'].browse(4066)
        # Lectura de los campos que pide el formulario ahora
        read_fields = ['name', 'propietario_id', 'marca_vehiculo_id', 'tipo', 'tipo_combustible', 'modelo', 'cilindraje', 'ingreso', 'pago_count', 'turno_count', 'conductor_ids']
        res_veh = v.read(read_fields)
        t1 = time.time()
        print("=== 1. FICHA DE VEHICULO OPTIMIZADA ===")
        print("  Vehiculo:", res_veh[0]['name'])
        print("  Propietario:", res_veh[0]['propietario_id'])
        print("  Pagos count (smart button):", res_veh[0]['pago_count'])
        print("  Despachos count (smart button):", res_veh[0]['turno_count'])
        print("  Conductores vinculados:", len(res_veh[0]['conductor_ids']))
        print("  Tiempo de lectura del formulario:", round(t1 - t0, 4), "s (Antes 1.12s)")
        print()

        # 2. Búsqueda de conductor al enturnar WGM776
        t2 = time.time()
        v_wgm = env['fundetaxcol.vehiculo'].search([('name', '=ilike', 'WGM776')], limit=1)
        turno_new = env['fundetaxcol.turno'].new({'bahia_id': 8816})
        turno_new.vehiculo_id = v_wgm
        turno_new._onchange_vehiculo_id()
        t3 = time.time()
        print("=== 2. ASIGNACIÓN EN TURNO ===")
        print("  Vehiculo:", v_wgm.name)
        print("  Conductor asignado:", turno_new.conductor_id.name)
        print("  Tiempo de _onchange_vehiculo_id():", round(t3 - t2, 4), "s")
        print()

        # 3. Búsqueda por Nombre de Conductor (ej: ISIDORO)
        t4 = time.time()
        conductores_nombre = env['res.partner'].name_search('ISIDORO', args=[('conductor', '=', True)], limit=5)
        t5 = time.time()
        print("=== 3. BÚSQUEDA POR NOMBRE ===")
        print("  Resultados para 'ISIDORO':", conductores_nombre)
        print("  Tiempo de name_search:", round(t5 - t4, 4), "s")
'''
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/verify_opt.py', 'w') as f:
        f.write(remote_code)
    sftp.close()

    _, stdout, stderr = ssh.exec_command('PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/verify_opt.py')
    print("STDOUT:")
    print(stdout.read().decode('utf-8'))
    print("STDERR:")
    print(stderr.read().decode('utf-8'))

    # También medir latencia del login web
    print("=== 4. LATENCIA HTTP LOGIN ===")
    for _ in range(2):
        _, stdout_curl, _ = ssh.exec_command("curl -o /dev/null -s -w 'HTTP %{http_code} | Total: %{time_total}s\\n' http://127.0.0.1:80/web/login")
        print(stdout_curl.read().decode('utf-8').strip())
        time.sleep(1)

    ssh.close()

if __name__ == '__main__':
    verify_improvements()
