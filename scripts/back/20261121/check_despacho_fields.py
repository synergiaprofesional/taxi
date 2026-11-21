import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

def run_cmd(title, cmd):
    print(f"\n=== {title} ===")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

run_cmd("BUSCAR ARCHIVOS DE TURNO", "find /opt -name '*turno*.py' 2>/dev/null")

run_cmd("BUSCAR DONDE ESTA FUNDETAXCOL", "find /opt -name 'fundetaxcol' 2>/dev/null")

run_cmd("BUSCAR DIRECCION EN IR_MODEL_FIELDS", """
sudo -u postgres psql -d fundetaxcol -c "SELECT model, name, field_description, ttype FROM ir_model_fields WHERE name LIKE '%dir%' OR name LIKE '%dest%' OR field_description ILIKE '%direcci%' ORDER BY model;"
""")

ssh.close()
