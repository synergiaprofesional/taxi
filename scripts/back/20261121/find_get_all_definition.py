import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

cmd = "grep -rn 'def get_all' /opt/synergia/addons_fundetaxcol/"
_, stdout, _ = ssh.exec_command(cmd)
print("--- DEF GET_ALL IN ADDONS ---")
print(stdout.read().decode('utf-8'))

ssh.close()
