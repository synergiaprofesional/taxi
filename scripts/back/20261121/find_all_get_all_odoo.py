import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

stdin, stdout, stderr = ssh.exec_command("grep -E 'addons_path' /opt/synergia/odoo-11.0/odoo_80.conf")
print(stdout.read().decode('utf-8', errors='ignore'))

# Buscar def get_all en esos addons
cmd = "grep -rn 'def get_all' /opt/synergia/odoo-11.0/addons/ /opt/synergia/ | grep -v '.git'"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("Definiciones de get_all:")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
