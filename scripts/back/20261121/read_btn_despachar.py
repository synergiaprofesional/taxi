import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "grep -rn 'def btn_despachar_turno' /opt/synergia/addons_fundetaxcol/ -A 35"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("BTN DESPACHAR:\n", stdout.read().decode('utf-8'))

ssh.close()
