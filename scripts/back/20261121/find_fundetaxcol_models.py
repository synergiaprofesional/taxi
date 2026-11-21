import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "grep -rn 'class.*Turno' /opt/synergia/addons_fundetaxcol/"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("TURNO CLASS:\n", stdout.read().decode('utf-8'))

cmd2 = "find /opt/synergia/addons_fundetaxcol -name '*.py'"
stdin, stdout, stderr = ssh.exec_command(cmd2)
print("PY FILES:\n", stdout.read().decode('utf-8'))

ssh.close()
