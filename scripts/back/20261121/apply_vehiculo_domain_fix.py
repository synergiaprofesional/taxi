import paramiko
import re

# 1. Update local file
local_path = r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\views\turno_view.xml'
with open(local_path, 'r', encoding='utf-8') as f:
    xml_content = f.read()

# Replace domain="[('id','in',vehiculo_ids)]" with domain="[('active','=',True)]"
old_str = "domain=\"[('id','in',vehiculo_ids)]\""
new_str = "domain=\"[('active','=',True)]\""

if old_str in xml_content:
    xml_content = xml_content.replace(old_str, new_str)
    with open(local_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print("Local turno_view.xml actualizado con éxito.")
else:
    print("WARNING: old_str no encontrado en local turno_view.xml")

# 2. Connect to server, upload, upgrade and restart
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=30)

server_path = '/opt/synergia/addons_fundetaxcol/fundetaxcol/views/turno_view.xml'
sftp = ssh.open_sftp()
with sftp.file(server_path, 'w') as f:
    f.write(xml_content)
sftp.close()
print("turno_view.xml subido a /opt/synergia/addons_fundetaxcol/fundetaxcol/views/turno_view.xml.")

print("\n--- EJECUTANDO UPGRADE EN ODOO 11 ---")
cmd_upgrade = "python3 /opt/synergia/odoo-11.0/odoo-bin -c /opt/synergia/odoo-11.0/odoo_80.conf -d fundetaxcol -u fundetaxcol --stop-after-init"
stdin, stdout, stderr = ssh.exec_command(cmd_upgrade)
out = stdout.read().decode('utf-8')
err = stderr.read().decode('utf-8')
print("Upgrade STDOUT:", out[-500:] if len(out) > 500 else out)
if "ERROR" in err:
    print("Upgrade STDERR ERRORS:", [line for line in err.splitlines() if "ERROR" in line])
else:
    print("Upgrade completado sin errores críticos.")

print("\n--- REINICIANDO SERVICIO ODOO_80 ---")
stdin, stdout, stderr = ssh.exec_command("systemctl restart odoo_80")
out = stdout.read().decode('utf-8')
print("Restart output:", out)

print("\n--- VERIFICANDO ESTADO DE ODOO_80 ---")
stdin, stdout, stderr = ssh.exec_command("systemctl is-active odoo_80")
print("Status odoo_80:", stdout.read().decode('utf-8').strip())

ssh.close()
print("Operación completada exitosamente.")
