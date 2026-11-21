import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "python3 -c \"import sys; [sys.path.append(p) for p in ['/opt/synergia/odoo-11.0', '/opt/synergia/addons']]; import odoo; odoo.tools.config.parse_config(['-c', '/opt/synergia/odoo.conf']); import odoo.modules.registry; reg = odoo.modules.registry.Registry('fundetaxcol'); cr = reg.cursor(); env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {}); import inspect; print('PAGO GET_ALL CODE:'); print(inspect.getsource(env['fundetaxcol.pago'].get_all)); cr.close()\""

stdin, stdout, stderr = ssh.exec_command(cmd)
print("OUT:\n", stdout.read().decode('utf-8', errors='ignore'))
print("ERR:\n", stderr.read().decode('utf-8', errors='ignore'))

ssh.close()
