import paramiko

def inspect_rt_service():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Inspeccionando server_rt_odoo y odoo_8069 en {host}...")
    ssh.connect(host, username=user, password=password, timeout=10)

    commands = [
        ("Definición server_rt_odoo.service", "cat /etc/systemd/system/server_rt_odoo.service"),
        ("Definición odoo_8069.service", "cat /etc/systemd/system/odoo_8069.service"),
        ("Estado de server_rt_odoo", "systemctl status server_rt_odoo.service --no-pager"),
        ("Logs recientes de server_rt_odoo", "journalctl -u server_rt_odoo.service -n 30 --no-pager"),
        ("Git status y remote en /opt/synergia/addons_fundetaxcol", "cd /opt/synergia/addons_fundetaxcol && git remote -v && git branch -a && git status -s")
    ]

    for title, cmd in commands:
        print(f"\n=======================================================")
        print(f"=== {title} ===")
        print(f"=======================================================")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore').strip()
        print(out)

    ssh.close()

if __name__ == "__main__":
    inspect_rt_service()
