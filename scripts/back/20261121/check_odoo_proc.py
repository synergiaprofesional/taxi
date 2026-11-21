import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

stdin, stdout, stderr = ssh.exec_command("ps aux | grep odoo")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
