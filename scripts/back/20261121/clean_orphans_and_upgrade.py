import paramiko
import time

def clean_orphans_and_upgrade():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=60)

    print("=== 1. ELIMINANDO 39 FILAS HUÉRFANAS EN FUNDETAXCOL_VEHICULO_PARTNER ===")
    sql_clean = """
    DELETE FROM fundetaxcol_vehiculo_partner 
    WHERE vehiculo_id NOT IN (SELECT id FROM fundetaxcol_vehiculo);
    """
    cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql_clean}\""
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    print("=== 2. DETENIENDO TEMPORALMENTE ODOO_80.SERVICE ===")
    ssh.exec_command("systemctl stop odoo_80.service")
    time.sleep(2)

    print("=== 3. RE-EJECUTANDO UPGRADE DE FUNDETAXCOL ===")
    cmd_upgrade = "PYTHONPATH=/opt/synergia/odoo-11.0 python3 /opt/synergia/odoo-11.0/odoo-bin -c /opt/synergia/odoo-11.0/odoo_80.conf -u fundetaxcol -d fundetaxcol --stop-after-init"
    _, stdout, stderr = ssh.exec_command(cmd_upgrade)
    
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    print("STDOUT:")
    print(out[-1500:] if len(out) > 1500 else out)
    print("STDERR:")
    print(err[-1500:] if len(err) > 1500 else err)

    print("=== 4. REINICIANDO ODOO_80.SERVICE ===")
    ssh.exec_command("systemctl start odoo_80.service")
    time.sleep(3)

    print("=== 5. COMPROBANDO LATENCIA Y ESTADO ===")
    _, stdout_curl, _ = ssh.exec_command("curl -o /dev/null -s -w 'HTTP Status: %{http_code} | Total: %{time_total}s\\n' http://127.0.0.1:80/web/login")
    print(stdout_curl.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    clean_orphans_and_upgrade()
