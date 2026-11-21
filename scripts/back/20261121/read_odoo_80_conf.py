import paramiko

def read_conf():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    cmd = "cat /opt/synergia/odoo-11.0/odoo_80.conf"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- /opt/synergia/odoo-11.0/odoo_80.conf ---")
    print(stdout.read().decode('utf-8'))

    # También ver puertos y memoria
    cmd2 = "free -h; nproc"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- MEMORIA Y CPUS ---")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_conf()
