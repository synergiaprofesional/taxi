import paramiko

def diagnose_indexes():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

    print("=== 1. SEQ SCAN VS IDX SCAN (TABLAS CON MÁS LECTURAS SECUENCIALES) ===")
    sql_scans = """
    SELECT relname, 
           n_live_tup, 
           seq_scan, 
           seq_tup_read, 
           idx_scan, 
           idx_tup_fetch,
           CASE WHEN (seq_scan + idx_scan) > 0 
                THEN round(seq_scan * 100.0 / (seq_scan + idx_scan), 2) 
                ELSE 0 
           END as pct_seq_scan
    FROM pg_stat_user_tables 
    WHERE n_live_tup > 1000 OR seq_scan > 500
    ORDER BY seq_tup_read DESC
    LIMIT 20;
    """
    cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql_scans}\""
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    print("=== 2. ÍNDICES EXISTENTES EN LAS TABLAS CRÍTICAS ===")
    sql_indexes = """
    SELECT tablename, indexname, indexdef 
    FROM pg_indexes 
    WHERE tablename IN (
        'fundetaxcol_turno', 
        'fundetaxcol_pago', 
        'fundetaxcol_sesion_bahia', 
        'fundetaxcol_bahia', 
        'fundetaxcol_pago_fundetaxcol_vehiculo_rel',
        'bus_bus'
    )
    ORDER BY tablename, indexname;
    """
    cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql_indexes}\""
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    print("=== 3. FOREIGN KEYS / COLUMNAS ID SIN ÍNDICE EN TABLAS GRANDES ===")
    sql_missing_fk = """
    WITH fk_columns AS (
        SELECT
            conname AS fk_name,
            conrelid::regclass AS table_name,
            a.attname AS fk_column
        FROM pg_constraint c
        JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
        WHERE c.contype = 'f'
    ),
    indexed_columns AS (
        SELECT
            indrelid::regclass AS table_name,
            a.attname AS index_column
        FROM pg_index i
        JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = i.indkey[0]
    )
    SELECT 
        fk.table_name,
        fk.fk_column,
        fk.fk_name
    FROM fk_columns fk
    LEFT JOIN indexed_columns ic 
        ON fk.table_name = ic.table_name AND fk.fk_column = ic.index_column
    WHERE ic.index_column IS NULL
      AND fk.table_name::text LIKE 'fundetaxcol_%'
    ORDER BY fk.table_name, fk.fk_column;
    """
    cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql_missing_fk}\""
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    print("=== 4. TAMAÑO DE ÍNDICES VS TAMAÑO DE TABLAS ===")
    sql_sizes = """
    SELECT
        relname AS table_name,
        pg_size_pretty(pg_relation_size(c.oid)) AS table_size,
        pg_size_pretty(pg_indexes_size(c.oid)) AS indexes_size,
        pg_size_pretty(pg_total_relation_size(c.oid)) AS total_size
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = 'public' 
      AND c.relkind = 'r'
      AND (c.relname LIKE 'fundetaxcol_%' OR c.relname IN ('bus_bus', 'mail_mail', 'mail_message'))
    ORDER BY pg_total_relation_size(c.oid) DESC
    LIMIT 15;
    """
    cmd = f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql_sizes}\""
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    diagnose_indexes()
