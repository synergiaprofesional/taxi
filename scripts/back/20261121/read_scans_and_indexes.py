import paramiko

def read_scans_and_indexes():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    print("=== SECCIÓN 1: SEQ SCAN VS IDX SCAN ===")
    sql = """
    SELECT relname, 
           n_live_tup, 
           seq_scan, 
           seq_tup_read, 
           idx_scan, 
           idx_tup_fetch,
           CASE WHEN (seq_scan + coalesce(idx_scan,0)) > 0 
                THEN round(seq_scan * 100.0 / (seq_scan + coalesce(idx_scan,0)), 2) 
                ELSE 0 
           END as pct_seq_scan
    FROM pg_stat_user_tables 
    WHERE n_live_tup > 500 OR seq_scan > 50
    ORDER BY seq_tup_read DESC
    LIMIT 25;
    """
    _, stdout, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql}\"")
    print(stdout.read().decode('utf-8'))

    print("=== SECCIÓN 2: ÍNDICES DE FUNDETAXCOL_TURNO ===")
    sql2 = "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'fundetaxcol_turno';"
    _, stdout2, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql2}\"")
    print(stdout2.read().decode('utf-8'))

    print("=== SECCIÓN 3: ÍNDICES DE FUNDETAXCOL_SESION_BAHIA ===")
    sql3 = "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'fundetaxcol_sesion_bahia';"
    _, stdout3, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql3}\"")
    print(stdout3.read().decode('utf-8'))

    print("=== SECCIÓN 4: ÍNDICES DE FUNDETAXCOL_PAGO ===")
    sql4 = "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'fundetaxcol_pago';"
    _, stdout4, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql4}\"")
    print(stdout4.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    read_scans_and_indexes()
