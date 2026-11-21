import paramiko
import time

def test_index_creation():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=30)

    print("=== CREANDO ÍNDICES CRÍTICOS CON CURRENTLY (CERO BLOQUEO) ===")
    indexes = [
        ("idx_turno_bahia_state", "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_turno_bahia_state ON fundetaxcol_turno (bahia_id, state);"),
        ("idx_turno_vehiculo_state", "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_turno_vehiculo_state ON fundetaxcol_turno (vehiculo_id, state);"),
        ("idx_turno_fecha_asig", "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_turno_fecha_asig ON fundetaxcol_turno (fecha_asignacion);"),
        ("idx_pago_bahia_fecha", "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_pago_bahia_fecha ON fundetaxcol_pago (bahia_id, fecha);"),
        ("idx_pago_vehiculo_fecha", "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_pago_vehiculo_fecha ON fundetaxcol_pago (vehiculo_id, fecha);"),
        ("idx_sesion_bahia_sesion_id", "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sesion_bahia_sesion_id ON fundetaxcol_sesion_bahia (sesion_id);"),
        ("idx_vehiculo_conductor_veh_id", "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_vehiculo_conductor_veh_id ON fundetaxcol_vehiculo_conductor (vehiculo_id);")
    ]

    for name, sql in indexes:
        t0 = time.time()
        print(f"Creando índice {name}...")
        cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql}\""
        _, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8').strip()
        err = stderr.read().decode('utf-8').strip()
        print(f"Resultado {name} ({time.time() - t0:.2f}s): {out} | {err}")

    print("\n=== EXPLAIN ANALYZE POST-ÍNDICE: TURNOS POR BAHÍA Y ESTADO ===")
    sql_test = """
    EXPLAIN (ANALYZE, BUFFERS) 
    SELECT id, name, vehiculo_id, state, fecha_asignacion 
    FROM fundetaxcol_turno 
    WHERE bahia_id = 8816 AND state != 'cancelado' 
    ORDER BY id DESC LIMIT 50;
    """
    cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql_test}\""
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    print("=== EXPLAIN ANALYZE POST-ÍNDICE: TURNO POR VEHÍCULO ===")
    sql_test2 = """
    EXPLAIN (ANALYZE, BUFFERS) 
    SELECT id, name, state 
    FROM fundetaxcol_turno 
    WHERE vehiculo_id = 4406 AND state = 'activo';
    """
    cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql_test2}\""
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    print("=== EXPLAIN ANALYZE POST-ÍNDICE: VEHICULO_CONDUCTOR ===")
    sql_test3 = """
    EXPLAIN (ANALYZE, BUFFERS) 
    SELECT id, conductor_id 
    FROM fundetaxcol_vehiculo_conductor 
    WHERE vehiculo_id = 4406;
    """
    cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql_test3}\""
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    test_index_creation()
