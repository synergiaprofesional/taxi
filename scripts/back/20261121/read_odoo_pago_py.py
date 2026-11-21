import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

cmd = "find /opt/synergia/addons/ -type f -name '*pago*.py' -exec grep -l 'def get_all' {} +"
stdin, stdout, stderr = ssh.exec_command(cmd)
files = stdout.read().decode('utf-8', errors='ignore').strip().split('\n')
print("Archivos con def get_all en pago:", files)

for f in files:
    if f:
        print(f"\n=== CONTENIDO DE {f} (seccion get_all) ===")
        cmd2 = f"grep -n 'def get_all' -A 40 {f}"
        stdin2, stdout2, stderr2 = ssh.exec_command(cmd2)
        print(stdout2.read().decode('utf-8', errors='ignore'))

ssh.close()
