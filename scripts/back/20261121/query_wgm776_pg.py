import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = """sudo -u postgres psql -d fundetaxcol -c "SELECT v.id, v.name, v.numero_interno, c.name as conductor, c.id as conductor_id FROM fundetaxcol_vehiculo v LEFT JOIN res_partner_fundetaxcol_vehiculo_rel r ON r.fundetaxcol_vehiculo_id = v.id LEFT JOIN res_partner c ON c.id = r.res_partner_id WHERE v.name = 'WGM776';" """

stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
