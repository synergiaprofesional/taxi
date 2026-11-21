import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "journalctl -u odoo_80 --since '15 minutes ago' -p err..warning --no-pager"
stdin, stdout, stderr = ssh.exec_command(cmd)
errs = stdout.read().decode('utf-8')
print("=== WARNINGS & ERRORS IN ODOO LOG ===")
print(errs if errs.strip() else "NO ERRORS OR WARNINGS LOGGED!")

cmd_http = "journalctl -u odoo_80 --since '15 minutes ago' --no-pager | grep -E '404|500|Exception|Traceback'"
stdin, stdout, stderr = ssh.exec_command(cmd_http)
http_errs = stdout.read().decode('utf-8')
print("=== HTTP 404/500 OR EXCEPTIONS ===")
print(http_errs if http_errs.strip() else "NO 404/500 OR TRACEBACKS LOGGED!")

ssh.close()
