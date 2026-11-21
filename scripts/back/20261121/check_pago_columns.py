import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = """sudo -u postgres psql -d fundetaxcol -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'fundetaxcol_pago';" """
stdin, stdout, stderr = ssh.exec_command(cmd)
print("=== COLUMNS OF fundetaxcol_pago ===")
print(stdout.read().decode('utf-8'))

ssh.close()
