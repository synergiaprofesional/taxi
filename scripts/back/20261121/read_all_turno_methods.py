import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "sed -n '1,120p' /opt/synergia/addons_fundetaxcol/fundetaxcol/models/turno_model.py"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("TURNO MODEL:\n", stdout.read().decode('utf-8'))

cmd2 = "sed -n '730,810p' /opt/synergia/addons_fundetaxcol/fundetaxcol_movil/models/models.py"
stdin, stdout, stderr = ssh.exec_command(cmd2)
print("TURNO MOVIL:\n", stdout.read().decode('utf-8'))

ssh.close()
