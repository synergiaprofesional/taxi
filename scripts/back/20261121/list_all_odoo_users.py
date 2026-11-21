import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = 'sudo -u postgres psql -d fundetaxcol -c "SELECT u.id, u.login, p.name FROM res_users u JOIN res_partner p ON u.partner_id = p.id WHERE u.active = true ORDER BY u.id;"'
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode('utf-8')
print("USERS:\n", out)

ssh.close()
