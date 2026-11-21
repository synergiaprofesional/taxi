import paramiko
import os
import tarfile

def sync_production_assets():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Conectando a {host} para empaquetar y descargar módulos de producción...")
    ssh.connect(host, username=user, password=password, timeout=10)

    # 1. Crear tarball en el servidor
    print("Empaquetando /opt/synergia/addons_fundetaxcol en el servidor...")
    cmd1 = "tar -czf /tmp/addons_fundetaxcol_prod.tar.gz -C /opt/synergia addons_fundetaxcol"
    stdin, stdout, stderr = ssh.exec_command(cmd1)
    stdout.channel.recv_exit_status()

    print("Empaquetando /opt/server_rt_odoo en el servidor...")
    cmd2 = "tar -czf /tmp/server_rt_odoo_prod.tar.gz -C /opt server_rt_odoo"
    stdin, stdout, stderr = ssh.exec_command(cmd2)
    stdout.channel.recv_exit_status()

    # 2. Descargar vía SFTP
    sftp = ssh.open_sftp()
    
    local_addons_tar = r"C:\Workspaces\addons_fundetaxcol_prod.tar.gz"
    local_rt_tar = r"C:\Workspaces\server_rt_odoo_prod.tar.gz"

    print(f"Descargando addons_fundetaxcol a {local_addons_tar}...")
    sftp.get("/tmp/addons_fundetaxcol_prod.tar.gz", local_addons_tar)

    print(f"Descargando server_rt_odoo a {local_rt_tar}...")
    sftp.get("/tmp/server_rt_odoo_prod.tar.gz", local_rt_tar)

    sftp.close()
    ssh.close()

    # 3. Descomprimir localmente
    print("Descomprimiendo localmente en C:\\Workspaces...")
    with tarfile.open(local_addons_tar, "r:gz") as tar:
        tar.extractall(path=r"C:\Workspaces")
    print("-> addons_fundetaxcol sincronizado en C:\\Workspaces\\addons_fundetaxcol")

    with tarfile.open(local_rt_tar, "r:gz") as tar:
        tar.extractall(path=r"C:\Workspaces")
    print("-> server_rt_odoo extraído en C:\\Workspaces\\server_rt_odoo")

    print("\n¡Descarga y sincronización de producción completada con éxito!")

if __name__ == "__main__":
    sync_production_assets()
