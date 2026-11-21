import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "python3 -c \"with open('/opt/synergia/addons_fundetaxcol/fundetaxcol_movil/models/models.py') as f: lines = f.readlines(); [print(f'{i+1}: {lines[i]}', end='') for i in range(310, 375)]\""
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
