import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_sql(query, title):
    print(f"\n=== {title} ===")
    cmd = f'sudo -u postgres psql -d fundetaxcol -c "{query}"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if out:
        print(out)
    if err and "could not change directory" not in err:
        print("ERR:", err)

run_sql("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'fundetaxcol_turno';", "COLUMNAS DE TURNO")
run_sql("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'fundetaxcol_pago';", "COLUMNAS DE PAGO")

ssh.close()
