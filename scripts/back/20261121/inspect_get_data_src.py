import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

script = """
import inspect
import odoo
from odoo import api
import odoo.tools.config as config
config.parse_config(['-c', '/opt/synergia/odoo-11.0/odoo_80.conf'])
registry = odoo.registry('fundetaxcol')
with odoo.api.Environment.manage():
    with registry.cursor() as cr:
        env = api.Environment(cr, odoo.SUPERUSER_ID, {})
        turno_cls = type(env['fundetaxcol.turno'])
        if hasattr(turno_cls, 'get_data'):
            print("SRC get_data:\\n", inspect.getsource(turno_cls.get_data))
        elif hasattr(turno_cls, '_get_data'):
            print("SRC _get_data:\\n", inspect.getsource(turno_cls._get_data))
        if hasattr(turno_cls, 'get_all'):
            print("SRC get_all:\\n", inspect.getsource(turno_cls.get_all))
"""

sftp = ssh.open_sftp()
with sftp.file('/tmp/check_src_get_data.py', 'w') as f:
    f.write(script)
sftp.close()

cmd = "PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/check_src_get_data.py"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("STDOUT:\n", stdout.read().decode('utf-8'))
err = stderr.read().decode('utf-8')
if "Traceback" in err:
    print("STDERR:\n", err)

ssh.close()

