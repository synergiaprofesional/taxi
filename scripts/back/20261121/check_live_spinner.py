import paramiko
import os
from dotenv import load_dotenv

load_dotenv()
SERVER_IP = os.getenv('ODOO_SERVER_IP', '149.22.88.135')
SERVER_USER = os.getenv('ODOO_SERVER_USER', 'root')
SERVER_PWD = os.getenv('ODOO_SERVER_PASSWORD', '2QoRhncZ')

def check_live_status():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)
    
    print("=== TOP PROCESSES & LOAD ===")
    stdin, stdout, stderr = ssh.exec_command("top -b -n 1 | head -n 15")
    print(stdout.read().decode('utf-8'))
    
    print("\n=== POSTGRES ACTIVE QUERIES ===")
    cmd_pg = """sudo -u postgres psql -d fundetaxcol -c "SELECT pid, age(clock_timestamp(), query_start), state, query FROM pg_stat_activity WHERE state != 'idle' AND pid <> pg_backend_pid();" """
    stdin, stdout, stderr = ssh.exec_command(cmd_pg)
    print(stdout.read().decode('utf-8'))
    
    print("\n=== LAST 30 LINES OF ODOO LOG ===")
    stdin, stdout, stderr = ssh.exec_command("tail -n 30 /var/log/odoo/odoo-server.log")
    print(stdout.read().decode('utf-8'))
    
    print("\n=== JOURNALCTL ODOO LAST 20 LINES ===")
    stdin, stdout, stderr = ssh.exec_command("journalctl -u odoo_80 -n 20 --no-pager")
    print(stdout.read().decode('utf-8'))
    
    ssh.close()

if __name__ == '__main__':
    check_live_status()
