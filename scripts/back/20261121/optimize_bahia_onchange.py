import paramiko

# 1. Update local turno_model.py
local_path = r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\models\turno_model.py'
with open(local_path, 'r', encoding='utf-8') as f:
    code = f.read()

old_onchange_bahia = """    @api.onchange('bahia_id')
    def _onchange_bahia_id(self):
        self.sequence = self.bahia_id.turno_actual
        pagos = self.env['fundetaxcol.pago']\\
            .search([('bahia_id','in', self.bahia_id.sesion_id.sesion_bahia_ids.ids)])
        turnos = self.env['fundetaxcol.turno']\\
            .search([('bahia_id','in', self.bahia_id.sesion_id.sesion_bahia_ids.ids)])
        self.vehiculo_ids = None
        for pago in pagos:
            ingreso = len(pago.concepto_ids.filtered(lambda x: \\
                x.concepto_id.clasificacion == 'cr_ingreso' \\
                    or x.concepto_id.clasificacion == 'ingreso'))
            if ingreso != 0:
                self.vehiculo_ids |= pago.vehiculo_id
        for turno in turnos:
            if turno.state == 'actual' or turno.state == 'espera' or turno.state == 'pausa':
                self.vehiculo_ids -= turno.vehiculo_id"""

new_onchange_bahia = """    @api.onchange('bahia_id')
    def _onchange_bahia_id(self):
        self.sequence = self.bahia_id.turno_actual"""

if old_onchange_bahia in code:
    code = code.replace(old_onchange_bahia, new_onchange_bahia)
    with open(local_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Local turno_model.py optimizado (_onchange_bahia_id aligerado).")
else:
    print("WARNING: old_onchange_bahia exact string not found in local turno_model.py")

# 2. Upload to server
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=30)

server_path = '/opt/synergia/addons_fundetaxcol/fundetaxcol/models/turno_model.py'
sftp = ssh.open_sftp()
with sftp.file(server_path, 'w') as f:
    f.write(code)
sftp.close()
print("turno_model.py subido al servidor.")

# 3. Restart Odoo service
stdin, stdout, stderr = ssh.exec_command("systemctl restart odoo_80")
print("Restart odoo_80:", stdout.read().decode('utf-8'))

stdin, stdout, stderr = ssh.exec_command("systemctl is-active odoo_80")
print("Status odoo_80:", stdout.read().decode('utf-8').strip())

ssh.close()
print("Optimización de backend completada.")
