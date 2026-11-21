import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

script = """
import os

os.system("grep -rn 'tablero_turnos' /opt/synergia/odoo-11.0/addons/ /opt/synergia/odoo-11.0/odoo/addons/ 2>/dev/null | head -n 30")
"""

sftp = ssh.open_sftp()
with sftp.file('/tmp/find_tablero.py', 'w') as f:
    f.write(script)
sftp.close()

cmd = "python3 /tmp/find_tablero.py"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("STDOUT:\n", stdout.read().decode('utf-8'))
err = stderr.read().decode('utf-8')
if err:
    print("STDERR:\n", err)

ssh.close()

