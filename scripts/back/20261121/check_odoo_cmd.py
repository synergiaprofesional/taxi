import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "ps aux | grep odoo"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("ODOO PROCESS:\n", stdout.read().decode('utf-8'))

ssh.close()
