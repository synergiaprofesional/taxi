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
        sesiones = env['fundetaxcol.sesion'].search([], order='id desc', limit=3)
        print(f"Ultimas sesiones:")
        for s in sesiones:
            print(f"  Sesion ID {s.id} - {s.name} - State: {s.state} - Fecha apertura: {s.fecha_apertura}")
            for sb in s.sesion_bahia_ids:
                total_pagos = len(sb.pago_ids)
                total_turnos = len(sb.turno_ids)
                print(f"    Bahia ID {sb.id} ({sb.bahia_id.name}) - State: {sb.state}: {total_pagos} pagos, {total_turnos} turnos")
                if total_pagos > 0:
                    p = sb.pago_ids[0]
                    print(f"      Ejemplo pago ID {p.id} consecutivo {p.consecutivo} _get_data():")
                    print(f"        {p._get_data()}")
'''

sftp = ssh.open_sftp()
with sftp.file('/tmp/check_last_sessions.py', 'w') as f:
    f.write(remote_code)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/check_last_sessions.py")
print("STDOUT:")
print(stdout.read().decode('utf-8'))

ssh.close()
