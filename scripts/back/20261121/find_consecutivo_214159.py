import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = """sudo -u postgres psql -d fundetaxcol -c "SELECT id, name, fecha, bahia_id, vehiculo_id, conductor_id, valor, consecutivo FROM fundetaxcol_pago WHERE consecutivo = '214159' OR vehiculo_id IN (SELECT id FROM fundetaxcol_vehiculo WHERE name = 'WGN741');" """
stdin, stdout, stderr = ssh.exec_command(cmd)
print("=== PAGO WITH CONSECUTIVO 214159 OR WGN741 ===")
print(stdout.read().decode('utf-8'))

cmd_conceptos = """sudo -u postgres psql -d fundetaxcol -c "SELECT pc.* FROM fundetaxcol_pago_concepto pc JOIN fundetaxcol_pago p ON pc.pago_id = p.id WHERE p.consecutivo = '214159';" """
stdin, stdout, stderr = ssh.exec_command(cmd_conceptos)
print("=== CONCEPTOS ===")
print(stdout.read().decode('utf-8'))

ssh.close()
