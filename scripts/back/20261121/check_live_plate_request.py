import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "journalctl -u odoo_80 --since '3 minutes ago' --no-pager"
stdin, stdout, stderr = ssh.exec_command(cmd)
logs = stdout.read().decode('utf-8')
print("=== LOGS LAST 3 MINUTES ===")
print(logs if logs.strip() else "NO LOGS IN THE LAST 3 MINUTES")

ssh.close()
