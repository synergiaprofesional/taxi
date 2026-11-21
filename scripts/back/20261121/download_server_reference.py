import os
import tarfile
import io
import paramiko

def download_server_reference():
    host = "fundetaxcol.co"
    user = "root"
    password = "2QoRhncZ"

    dest_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reference"))
    os.makedirs(dest_dir, exist_ok=True)
    os.makedirs(os.path.join(dest_dir, "config"), exist_ok=True)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Conectando a {host} (MODO ESTRICTO SOLO LECTURA)...")
    ssh.connect(host, username=user, password=password, timeout=15)
    print("Conectado exitosamente.")

    # 1. Descargar config files directamente por SFTP (read-only)
    sftp = ssh.open_sftp()
    config_files = [
        ("/etc/caddy/Caddyfile", os.path.join(dest_dir, "config", "Caddyfile")),
        ("/opt/synergia/odoo-11.0/odoo_80.conf", os.path.join(dest_dir, "config", "odoo_80.conf")),
        ("/etc/systemd/system/odoo_80.service", os.path.join(dest_dir, "config", "odoo_80.service")),
    ]
    for remote, local in config_files:
        try:
            print(f"Descargando config: {remote} -> {local}")
            sftp.get(remote, local)
        except Exception as e:
            print(f"Nota: no se pudo leer {remote}: {e}")
    sftp.close()

    # 2. Descargar /opt/server_rt_odoo sin node_modules vía tar stream
    print("\nDescargando /opt/server_rt_odoo (sin node_modules) mediante streaming tar en memoria...")
    cmd_rt = "tar --exclude='node_modules' --exclude='.git' -czf - -C /opt server_rt_odoo"
    stdin, stdout, stderr = ssh.exec_command(cmd_rt)
    tar_rt_bytes = stdout.read()
    err_rt = stderr.read().decode('utf-8', errors='ignore')
    if err_rt:
        print(f"stderr rt: {err_rt}")
    
    with tarfile.open(fileobj=io.BytesIO(tar_rt_bytes), mode="r:gz") as tar:
        tar.extractall(path=dest_dir)
    print("server_rt_odoo extraído con éxito en reference/server_rt_odoo")

    # 3. Descargar /opt/synergia/addons_fundetaxcol vía tar stream
    print("\nDescargando /opt/synergia/addons_fundetaxcol mediante streaming tar en memoria...")
    cmd_addons = "tar --exclude='.git' --exclude='*.pyc' --exclude='__pycache__' -czf - -C /opt/synergia addons_fundetaxcol"
    stdin, stdout, stderr = ssh.exec_command(cmd_addons)
    tar_addons_bytes = stdout.read()
    err_addons = stderr.read().decode('utf-8', errors='ignore')
    if err_addons:
        print(f"stderr addons: {err_addons}")
    
    with tarfile.open(fileobj=io.BytesIO(tar_addons_bytes), mode="r:gz") as tar:
        tar.extractall(path=dest_dir)
    print("addons_fundetaxcol extraído con éxito en reference/addons_fundetaxcol")

    ssh.close()
    print("\nProceso de respaldo de referencia finalizado con éxito sin escribir NADA en el servidor.")

if __name__ == "__main__":
    download_server_reference()
