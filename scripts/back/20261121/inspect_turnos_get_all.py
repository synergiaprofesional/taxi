import paramiko

def inspect_turnos():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    # Let's inspect recent turnos
    cmd = '''sudo -u postgres psql -d fundetaxcol -c "SELECT id, name, sequence, state, vehiculo_id, conductor_id, bahia_id, anonimo, placa_anonima FROM fundetaxcol_turno ORDER BY id DESC LIMIT 10;"'''
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("--- 10 TURNOS RECIENTES ---")
    print(stdout.read().decode('utf-8'))

    # Let's check how fundetaxcol.turno get_all is implemented in python in odoo
    cmd2 = '''grep -rn "def get_all" /opt/odoo/ /var/log/ /etc/odoo/ /home/ 2>/dev/null || true'''
    stdin, stdout, stderr = ssh.exec_command(cmd2)
    print("--- DEF GET_ALL IN ODOO ---")
    print(stdout.read().decode('utf-8')[:1500])

    ssh.close()

if __name__ == '__main__':
    inspect_turnos()
