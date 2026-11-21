import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

cmd = "python3 -c 'with open(\"/opt/synergia/addons_fundetaxcol/fundetaxcol_movil/models/models.py\") as f: lines = f.readlines(); [print(f\"{i+1}: {lines[i]}\", end=\"\") for i in range(300, 360)]'"
_, stdout, _ = ssh.exec_command(cmd)
print("--- LINES 301-360 ---")
print(stdout.read().decode('utf-8'))

cmd2 = "python3 -c 'with open(\"/opt/synergia/addons_fundetaxcol/fundetaxcol_movil/models/models.py\") as f: lines = f.readlines(); [print(f\"{i+1}: {lines[i]}\", end=\"\") for i in range(680, 720)]'"
_, stdout2, _ = ssh.exec_command(cmd2)
print("--- LINES 681-720 ---")
print(stdout2.read().decode('utf-8'))

ssh.close()
