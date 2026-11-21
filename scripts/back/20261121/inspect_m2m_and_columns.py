import paramiko

def inspect_m2m_and_columns():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    print("=== ÍNDICES DE TABLAS RELACIONALES MANY2MANY ===")
    sql = """
    SELECT tablename, indexname, indexdef 
    FROM pg_indexes 
    WHERE tablename IN (
        'fundetaxcol_pago_fundetaxcol_vehiculo_rel',
        'fundetaxcol_turno_fundetaxcol_vehiculo_rel',
        'fundetaxcol_pago_res_partner_rel',
        'fundetaxcol_turno_res_partner_rel'
    );
    """
    _, stdout, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql}\"")
    print(stdout.read().decode('utf-8'))

    print("=== COLUMNAS PRINCIPALES DE FUNDETAXCOL_TURNO ===")
    sql2 = """
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'fundetaxcol_turno' 
    ORDER BY ordinal_position;
    """
    _, stdout2, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql2}\"")
    print(stdout2.read().decode('utf-8'))

    print("=== COLUMNAS PRINCIPALES DE FUNDETAXCOL_PAGO ===")
    sql3 = """
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'fundetaxcol_pago' 
    ORDER BY ordinal_position;
    """
    _, stdout3, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql3}\"")
    print(stdout3.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    inspect_m2m_and_columns()
