import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "head -n 100 /opt/synergia/addons_fundetaxcol/fundetaxcol/static/src/js/z_tablero_turno.js"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("z_tablero_turno.js:\n", stdout.read().decode('utf-8'))

ssh.close()

