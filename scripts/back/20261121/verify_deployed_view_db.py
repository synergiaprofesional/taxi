import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = """sudo -u postgres psql -d fundetaxcol -c "SELECT arch_db FROM ir_ui_view WHERE id IN (SELECT res_id FROM ir_model_data WHERE module='fundetaxcol' AND name='asignar_turno_form');" """
stdin, stdout, stderr = ssh.exec_command(cmd)
res = stdout.read().decode('utf-8')
print("=== DEPLOYED ARCH IN DB ===")
print([line for line in res.splitlines() if 'vehiculo_id' in line])

ssh.close()
