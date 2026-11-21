import paramiko

def inspect_query_plans():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    print("=== COLUMNAS DE FUNDETAXCOL_SESION_BAHIA ===")
    sql = """
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'fundetaxcol_sesion_bahia' 
    ORDER BY ordinal_position;
    """
    _, stdout, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql}\"")
    print(stdout.read().decode('utf-8'))

    print("=== EXPLAIN ANALYZE: QUERY TÍPICO DE TURNOS POR BAHÍA Y ESTADO ===")
    sql2 = """
    EXPLAIN (ANALYZE, BUFFERS) 
    SELECT id, name, vehiculo_id, state, fecha_asignacion 
    FROM fundetaxcol_turno 
    WHERE bahia_id = 1 AND state != 'cancelado' 
    ORDER BY id DESC LIMIT 50;
    """
    _, stdout2, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql2}\"")
    print(stdout2.read().decode('utf-8'))

    print("=== EXPLAIN ANALYZE: QUERY TÍPICO DE TURNOS POR VEHÍCULO ===")
    sql3 = """
    EXPLAIN (ANALYZE, BUFFERS) 
    SELECT id, name, state 
    FROM fundetaxcol_turno 
    WHERE vehiculo_id = 100 AND state = 'activo';
    """
    _, stdout3, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql3}\"")
    print(stdout3.read().decode('utf-8'))

    print("=== EXPLAIN ANALYZE: QUERY TÍPICO DE PAGOS POR VEHÍCULO ===")
    sql4 = """
    EXPLAIN (ANALYZE, BUFFERS) 
    SELECT id, consecutivo, fecha, valor 
    FROM fundetaxcol_pago 
    WHERE vehiculo_id = 100 
    ORDER BY fecha DESC LIMIT 10;
    """
    _, stdout4, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql4}\"")
    print(stdout4.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    inspect_query_plans()
