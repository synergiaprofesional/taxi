import paramiko
import os

def sync_local_addons():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)
    sftp = ssh.open_sftp()

    files_to_sync = [
        ('/opt/synergia/addons_fundetaxcol/fundetaxcol/models/vehiculo_model.py', r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\models\vehiculo_model.py'),
        ('/opt/synergia/addons_fundetaxcol/fundetaxcol/views/vehiculo_view.xml', r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\views\vehiculo_view.xml'),
        ('/opt/synergia/addons_fundetaxcol/fundetaxcol/models/turno_model.py', r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\models\turno_model.py'),
        ('/opt/synergia/addons_fundetaxcol/fundetaxcol/views/turno_view.xml', r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\views\turno_view.xml'),
        ('/opt/synergia/addons_fundetaxcol/fundetaxcol/models/conductor_model.py', r'C:\Workspaces\addons_fundetaxcol\fundetaxcol\models\conductor_model.py'),
    ]

    for remote_path, local_path in files_to_sync:
        print(f"Descargando {remote_path} -> {local_path}")
        sftp.get(remote_path, local_path)

    sftp.close()
    ssh.close()
    print("Sincronización local completada.")

if __name__ == '__main__':
    sync_local_addons()
