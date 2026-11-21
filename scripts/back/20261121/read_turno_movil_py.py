import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "sed -n '670,760p' /opt/synergia/addons_fundetaxcol/fundetaxcol_movil/models/models.py"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("TURNO MOVIL:\n", stdout.read().decode('utf-8'))

ssh.close()
