import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "sed -n '800,860p' /opt/synergia/addons_fundetaxcol/fundetaxcol_movil/models/models.py"
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode('utf-8'))

ssh.close()
