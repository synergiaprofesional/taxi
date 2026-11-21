import paramiko

def check_odoo_health():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    print("=== CRONS ACTIVOS Y SUS PRÓXIMAS EJECUCIONES ===")
    cmd_cron = """cd /tmp && sudo -u postgres psql -d fundetaxcol -c "
    SELECT id, name, interval_number, interval_type, numbercall, nextcall, active 
    FROM ir_cron 
    WHERE active = true 
    ORDER BY nextcall ASC;"
    """
    _, stdout, _ = ssh.exec_command(cmd_cron)
    print(stdout.read().decode('utf-8'))

    print("=== ÚLTIMAS 30 LÍNEAS DE LOG DE ODOO ===")
    cmd_log = "journalctl -u odoo_80.service -n 30 --no-pager"
    _, stdout, _ = ssh.exec_command(cmd_log)
    print(stdout.read().decode('utf-8'))

    print("=== MONITOREO DE PROCESO ODOO ===")
    cmd_top = "top -b -n 1 | head -n 15"
    _, stdout, _ = ssh.exec_command(cmd_top)
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_odoo_health()
