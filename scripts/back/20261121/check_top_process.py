import paramiko

def check_cpu_process():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    print("=== TOP PROCESOS POR CPU ===")
    cmd = "ps aux --sort=-%cpu | head -n 10"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    print("=== HILOS DEL PROCESO QUE MÁS CONSUME ===")
    cmd2 = "top -H -b -n 1 -p $(pgrep -f odoo-bin | head -n 1) | head -n 15"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print(stdout2.read().decode('utf-8'))

    print("=== BUSCAR OTROS CRONS FALLANDO ===")
    cmd3 = "sudo -u postgres psql -d fundetaxcol -c 'SELECT id, name, model, interval_number, interval_type, numbercall, nextcall, active FROM ir_cron WHERE active=true ORDER BY nextcall;'"
    _, stdout3, _ = ssh.exec_command(cmd3)
    print(stdout3.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_cpu_process()
