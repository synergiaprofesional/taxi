import paramiko

def inspect_node_service():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Inspeccionando /opt/server_rt_odoo en {host}...")
    ssh.connect(host, username=user, password=password, timeout=10)

    commands = [
        ("Listado /opt/server_rt_odoo", "ls -la /opt/server_rt_odoo/"),
        ("package.json", "cat /opt/server_rt_odoo/package.json 2>/dev/null || echo 'No package.json'"),
        ("src/index.js", "head -n 60 /opt/server_rt_odoo/src/index.js 2>/dev/null || echo 'No index.js'"),
        ("Por que fallo o se detuvo", "journalctl -u server_rt_odoo -n 20 --no-pager 2>/dev/null || echo 'Sin logs'")
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
    inspect_node_service()
