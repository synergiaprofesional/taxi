import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

script = """
import odoo
from odoo import api
import odoo.tools.config as config
config.parse_config(['-c', '/opt/synergia/odoo-11.0/odoo_80.conf'])
registry = odoo.registry('fundetaxcol')
with odoo.api.Environment.manage():
    with registry.cursor() as cr:
        env = api.Environment(cr, odoo.SUPERUSER_ID, {})
        bays = env['fundetaxcol.sesion.bahia'].search([('state', '=', 'progreso')])
        print("BAHIAS EN PROGRESO:", [(b.id, b.name, b.bahia_id.name) for b in bays])
        bay_ids = bays.ids
        
        turnos_all = env['fundetaxcol.turno'].get_all(bahia_ids=bay_ids)
        print("TOTAL get_all turnos:", len(turnos_all))
        for t in turnos_all:
            b_id = t.get('bahia_id')
            print(f"ID: {t.get('id')} | Seq: {t.get('sequence')} | Name: {t.get('name')} | State: {t.get('state')} | Bahia: {b_id}")
"""

sftp = ssh.open_sftp()
with sftp.file('/tmp/test_turnos.py', 'w') as f:
    f.write(script)
sftp.close()

cmd = "PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/test_turnos.py"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("STDOUT:\n", stdout.read().decode('utf-8'))
err = stderr.read().decode('utf-8')
if "Traceback" in err:
    print("STDERR:\n", err)

ssh.close()
