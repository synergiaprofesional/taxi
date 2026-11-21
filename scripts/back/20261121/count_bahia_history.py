import paramiko

def count_bahia_history():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    print("=== TURNOS Y PAGOS ASOCIADOS A LA SESIÓN / BAHÍA ACTUAL ===")
    sql = """
    SELECT s.id as sesion_id, s.name, sb.id as sesion_bahia_id, sb.name as bahia_name,
           (SELECT count(*) FROM fundetaxcol_turno t WHERE t.bahia_id = sb.id) as total_turnos_bahia,
           (SELECT count(*) FROM fundetaxcol_pago p WHERE p.bahia_id = sb.id) as total_pagos_bahia
    FROM fundetaxcol_sesion_bahia sb
    JOIN fundetaxcol_sesion s ON s.id = sb.sesion_id
    WHERE s.state = 'en_progreso' OR s.id = (SELECT max(id) FROM fundetaxcol_sesion);
    """
    _, stdout, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql}\"")
    print(stdout.read().decode('utf-8'))

    print("=== TOTAL TURNOS Y PAGOS AGRUPADOS POR BAHIA_ID EN FUNDETAXCOL_TURNO ===")
    sql2 = """
    SELECT bahia_id, count(*) 
    FROM fundetaxcol_turno 
    GROUP BY bahia_id 
    ORDER BY count(*) DESC 
    LIMIT 10;
    """
    _, stdout2, _ = ssh.exec_command(f"cd /tmp && sudo -u postgres psql -d fundetaxcol -c \"{sql2}\"")
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    count_bahia_history()
