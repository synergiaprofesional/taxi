import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = """sudo -u postgres psql -d fundetaxcol -c "SELECT * FROM fundetaxcol_pago WHERE name = '214159' OR id = 214159;" """
stdin, stdout, stderr = ssh.exec_command(cmd)
print("=== PAGO RECORD 214159 ===")
print(stdout.read().decode('utf-8'))

cmd_conceptos = """sudo -u postgres psql -d fundetaxcol -c "SELECT pc.* FROM fundetaxcol_pago_concepto pc JOIN fundetaxcol_pago p ON pc.pago_id = p.id WHERE p.name = '214159' OR p.id = 214159;" """
stdin, stdout, stderr = ssh.exec_command(cmd_conceptos)
print("=== PAGO CONCEPTOS FOR 214159 ===")
print(stdout.read().decode('utf-8'))

ssh.close()
