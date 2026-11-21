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
        # Turnos en sesion 8867 (Garita)
        cr.execute('''
            SELECT t.id, t.sequence, v.name as placa, p.name as conductor, t.state, t.create_date, t.fecha_despacho, t.valor, sec.name as destino
            FROM fundetaxcol_turno t
            LEFT JOIN fundetaxcol_vehiculo v ON t.vehiculo_id = v.id
            LEFT JOIN res_partner p ON t.conductor_id = p.id
            LEFT JOIN fundetaxcol_tarifa_sector sec ON t.tarifa_id = sec.id
            WHERE t.bahia_id = 8867
            ORDER BY t.sequence ASC;
        ''')
        rows = cr.fetchall()
        print("TURNOS EN SESION 8867 (Garita):")
        for r in rows:
            print(f"Seq: {r[1]} | Placa: {r[2]} | Cond: {r[3]} | State: {r[4]} | create_date (UTC): {r[5]} | fecha_despacho (UTC): {r[6]} | valor: {r[7]} | destino: {r[8]}")
"""

sftp = ssh.open_sftp()
with sftp.file('/tmp/check_garita_8867.py', 'w') as f:
    f.write(script)
sftp.close()

cmd = "PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/check_garita_8867.py"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("STDOUT:\n", stdout.read().decode('utf-8'))
err = stderr.read().decode('utf-8')
if "Traceback" in err:
    print("STDERR:\n", err)

ssh.close()
