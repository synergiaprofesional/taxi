import paramiko
from datetime import datetime

def backup_server_addons():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = "/opt/synergia/backups_addons"
    backup_file = f"{backup_dir}/addons_fundetaxcol_backup_{timestamp}.tar.gz"

    print(f"=== CREANDO BACKUP DE RESGUARDO EN EL SERVIDOR ===")
    cmd = f"""
    mkdir -p {backup_dir} && 
    tar -czvf {backup_file} -C /opt/synergia addons_fundetaxcol && 
    ls -lh {backup_file}
    """
    _, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    print("STDOUT:")
    print(out)
    if err:
        print("STDERR:")
        print(err)

    ssh.close()

if __name__ == '__main__':
    backup_server_addons()
