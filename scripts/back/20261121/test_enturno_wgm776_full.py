import paramiko

def test_enturno_wgm776():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=20)

    remote_code = '''
import odoo
from odoo import api, SUPERUSER_ID
import time

config_path = '/opt/synergia/odoo-11.0/odoo_80.conf'
odoo.tools.config.parse_config(['-c', config_path])
registry = odoo.registry('fundetaxcol')

with api.Environment.manage():
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # ==============================================================
        # PARTE 1: AUDITORÍA DE LA FICHA DEL VEHÍCULO WGM776
        # ==============================================================
        print("=== 1. AUDITORÍA DEL VEHÍCULO WGM776 ===")
        t0 = time.time()
        vehiculo = env['fundetaxcol.vehiculo'].search([('name', '=ilike', 'WGM776')], limit=1)
        if not vehiculo:
            print("ERROR: No se encontró WGM776")
            exit()
            
        placa = vehiculo.name
        propietario = vehiculo.propietario_id.name if vehiculo.propietario_id else "Sin propietario"
        conductores = [f"{cp.sequence}: {cp.conductor_id.name} (ID {cp.conductor_id.id})" for cp in vehiculo.conductor_ids]
        ingreso_mes = vehiculo.ingreso
        total_pagos = len(vehiculo.pago_ids)
        total_turnos = len(vehiculo.turno_ids)
        t1 = time.time()
        
        print(f"  Placa: {placa} (ID: {vehiculo.id})")
        print(f"  Propietario: {propietario}")
        print(f"  Conductores en pestaña Conductores: {conductores}")
        print(f"  Ingresos mes: {ingreso_mes}")
        print(f"  Total Pagos históricos: {total_pagos}")
        print(f"  Total Despachos históricos: {total_turnos}")
        print(f"  Tiempo de carga de la ficha del vehículo: {round(t1 - t0, 4)} s")
        print()

        # ==============================================================
        # PARTE 2: SIMULACIÓN EXACTA DEL ENTURNADO EN GARITA
        # ==============================================================
        print("=== 2. SIMULACIÓN PASO A PASO DEL ENTURNADO EN BAHÍA ===")
        bahia = env['fundetaxcol.sesion.bahia'].browse(8816) # Garita
        print(f"  Bahía destino: {bahia.name} (Turno actual en bahía: {bahia.turno_actual})")

        # Paso 2.1: El cajero abre la pantalla "Nuevo Turno"
        t_open = time.time()
        turno_nuevo = env['fundetaxcol.turno'].new({
            'bahia_id': bahia.id,
            'company_id': 1
        })
        t_open_end = time.time()
        print(f"  Paso 2.1 - Apertura de pantalla Nuevo Turno: {round(t_open_end - t_open, 4)} s")

        # Paso 2.2: Odoo ejecuta _onchange_bahia_id (filtra qué taxis pagaron hoy y no están en cola)
        t_bahia = time.time()
        turno_nuevo._onchange_bahia_id()
        t_bahia_end = time.time()
        print(f"  Paso 2.2 - _onchange_bahia_id() (validación de pagos hoy): {round(t_bahia_end - t_bahia, 4)} s")
        print(f"             Vehículos habilitados para enturnar: {len(turno_nuevo.vehiculo_ids)}")
        print(f"             ¿Está WGM776 habilitado?: {vehiculo.id in turno_nuevo.vehiculo_ids.ids}")

        # Paso 2.3: El cajero digita y selecciona WGM776 ➔ Se dispara _onchange_vehiculo_id
        t_veh = time.time()
        turno_nuevo.vehiculo_id = vehiculo
        turno_nuevo._onchange_vehiculo_id()
        t_veh_end = time.time()
        print(f"  Paso 2.3 - _onchange_vehiculo_id(): {round(t_veh_end - t_veh, 4)} s")
        print(f"             Conductor auto-asignado: {turno_nuevo.conductor_id.name if turno_nuevo.conductor_id else 'NINGUNO'}")
        print(f"             Filtro de conductores disponibles: {[c.name for c in turno_nuevo.conductor_ids]}")

        # Paso 2.4: Llamada completa del cliente web de Odoo (RPC onchange)
        t_rpc = time.time()
        specs = {
            'vehiculo_id': '1',
            'conductor_id': '1',
            'conductor_ids': '1',
            'vehiculo_ids': '1',
            'bahia_id': '1',
            'sequence': '1'
        }
        values = {
            'bahia_id': bahia.id,
            'vehiculo_id': vehiculo.id,
            'conductor_id': False,
            'sequence': bahia.turno_actual
        }
        res_rpc = env['fundetaxcol.turno'].onchange(values, ['vehiculo_id'], specs)
        t_rpc_end = time.time()
        print(f"  Paso 2.4 - Respuesta RPC completa enviada al navegador: {round(t_rpc_end - t_rpc, 4)} s")
        print(f"             Payload devuelto al navegador: {res_rpc.get('value', {})}")

        # Paso 2.5: Simular la confirmación del turno (sin commit para no alterar datos de producción)
        t_create = time.time()
        vals_create = {
            'bahia_id': bahia.id,
            'vehiculo_id': vehiculo.id,
            'conductor_id': turno_nuevo.conductor_id.id,
            'sequence': bahia.turno_actual,
            'state': 'espera'
        }
        # Creamos y medimos
        test_turno = env['fundetaxcol.turno'].create(vals_create)
        t_create_end = time.time()
        print(f"  Paso 2.5 - Creación del Turno en Base de Datos: {round(t_create_end - t_create, 4)} s")
        print(f"             Turno generado: {test_turno.name} (ID: {test_turno.id}, Secuencia: #{test_turno.sequence})")

        # Rollback para dejar la base de datos de producción intacta
        cr.rollback()
        print("  [Rollback ejecutado: no se guardaron registros de prueba]")
'''
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/bench_enturno_wgm776.py', 'w') as f:
        f.write(remote_code)
    sftp.close()

    _, stdout, stderr = ssh.exec_command('PYTHONPATH=/opt/synergia/odoo-11.0 python3 /tmp/bench_enturno_wgm776.py')
    print("STDOUT:")
    print(stdout.read().decode('utf-8'))
    print("STDERR:")
    print(stderr.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    test_enturno_wgm776()
