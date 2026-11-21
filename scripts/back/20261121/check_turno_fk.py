import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "sudo -u postgres psql -d fundetaxcol -c \"SELECT id, name, bahia_id, state FROM fundetaxcol_turno ORDER BY id DESC LIMIT 10;\""
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode('utf-8', errors='ignore'))

# Y ver definicion de foreign key de bahia_id en fundetaxcol_pago y fundetaxcol_turno
cmd_fk = """sudo -u postgres psql -d fundetaxcol -c "
SELECT conname, conrelid::regclass, confrelid::regclass 
FROM pg_constraint 
WHERE conname IN ('fundetaxcol_pago_bahia_id_fkey', 'fundetaxcol_turno_bahia_id_fkey');"
"""
stdin2, stdout2, stderr2 = ssh.exec_command(cmd_fk)
print(stdout2.read().decode('utf-8', errors='ignore'))

ssh.close()
