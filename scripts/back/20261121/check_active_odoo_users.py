import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = """sudo -u postgres psql -d fundetaxcol -c "SELECT id, login, active FROM res_users WHERE active=true;" """
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode('utf-8'))

ssh.close()
