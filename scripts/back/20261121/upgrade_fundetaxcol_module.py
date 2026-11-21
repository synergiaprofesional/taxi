import paramiko
import time

def upgrade_module():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=60)

    print("=== 1. DETENIENDO TEMPORALMENTE ODOO_80.SERVICE ===")
    ssh.exec_command("systemctl stop odoo_80.service")
    time.sleep(2)

    print("=== 2. ACTUALIZANDO MÓDULO FUNDETAXCOL CON ODOO-BIN ===")
    cmd_upgrade = "PYTHONPATH=/opt/synergia/odoo-11.0 python3 /opt/synergia/odoo-11.0/odoo-bin -c /opt/synergia/odoo-11.0/odoo_80.conf -u fundetaxcol -d fundetaxcol --stop-after-init"
    _, stdout, stderr = ssh.exec_command(cmd_upgrade)
    
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    print("STDOUT:")
    print(out[-2000:] if len(out) > 2000 else out)
    print("STDERR:")
    print(err[-2000:] if len(err) > 2000 else err)

    print("=== 3. REINICIANDO ODOO_80.SERVICE ===")
    ssh.exec_command("systemctl start odoo_80.service")
    time.sleep(3)

    print("=== 4. VERIFICANDO ESTADO DEL SERVICIO ===")
    _, stdout_status, _ = ssh.exec_command("systemctl status odoo_80.service | head -n 15")
    print(stdout_status.read().decode('utf-8'))

    print("=== 5. PROBANDO LATENCIA HTTP ===")
    _, stdout_curl, _ = ssh.exec_command("curl -o /dev/null -s -w 'HTTP Status: %{http_code} | Total: %{time_total}s\\n' http://127.0.0.1:80/web/login")
    print(stdout_curl.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    upgrade_module()
