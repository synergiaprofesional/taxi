import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "ls -la /opt/synergia/addons"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("ADDONS:\n", stdout.read().decode('utf-8'))

cmd2 = "find /opt/synergia/addons -name '*turno*.py'"
stdin, stdout, stderr = ssh.exec_command(cmd2)
print("TURNO FILES:\n", stdout.read().decode('utf-8'))

ssh.close()
