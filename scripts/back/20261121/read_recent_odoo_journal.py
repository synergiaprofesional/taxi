import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "journalctl -u odoo_80 --since '10 minutes ago' --no-pager"
stdin, stdout, stderr = ssh.exec_command(cmd)
logs = stdout.read().decode('utf-8')
print("Total log length:", len(logs))
lines = logs.splitlines()
print(f"Total lines: {len(lines)}")
for l in lines[-60:]:
    print(l)

ssh.close()
