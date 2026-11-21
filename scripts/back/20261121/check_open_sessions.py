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
        # Buscar todas las sesiones abiertas hoy
        sesiones = env['fundetaxcol.sesion'].search([('state', '=', 'abierta')])
        print(f"Sesiones abiertas: {len(sesiones)}")
        for s in sesiones:
            print(f"  Sesion ID {s.id} - {s.name} - Fecha: {s.fecha_apertura}")
            for sb in s.sesion_bahia_ids:
                total_pagos = len(sb.pago_ids)
                total_turnos = len(sb.turno_ids)
                print(f"    Bahia ID {sb.id} ({sb.bahia_id.name}): {total_pagos} pagos, {total_turnos} turnos")
'''

sftp = ssh.open_sftp()
with sftp.file('/tmp/check_sessions_today.py', 'w') as f:
    f.write(remote_code)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/check_sessions_today.py")
print("STDOUT:")
print(stdout.read().decode('utf-8'))
print("STDERR:")
print(stderr.read().decode('utf-8'))

ssh.close()
