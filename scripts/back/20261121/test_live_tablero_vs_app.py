import xmlrpc.client

url = 'http://fundetaxcol.co'
db = 'fundetaxcol'
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, 'garita@fundetaxcol.co', '2QoRhncZ', {})
print("UID:", uid)

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# 1. Sesiones de bahia abiertas
bays = models.execute_kw(db, uid, '2QoRhncZ', 'fundetaxcol.sesion.bahia', 'search_read', [
    [['state', '=', 'progreso']]
], {'fields': ['id', 'name', 'bahia_id', 'sesion_id', 'turno_actual_id']})
print("\n=== BAHIAS EN PROGRESO ===")
for b in bays:
    print(b)

bay_ids = [b['id'] for b in bays]
print("\nBay IDs:", bay_ids)

# 2. search_read en fundetaxcol.turno exactamente como tablero_turnos
print("\n=== TURNOS SEARCH_READ COMO TABLERO_TURNOS (Garita 8843) ===")
turnos_garita = models.execute_kw(db, uid, '2QoRhncZ', 'fundetaxcol.turno', 'search_read', [
    [
        ['bahia_id', '=', 8843],
        ['state', 'not in', ['cancelado', 'despachado']]
    ]
], {'fields': ['id', 'name', 'state', 'sequence', 'vehiculo_id', 'conductor_id', 'bahia_id', 'anonimo']})
for t in turnos_garita:
    print(t)

print("\n=== TURNOS SEARCH_READ COMO TABLERO_TURNOS (29D 8842) ===")
turnos_29d = models.execute_kw(db, uid, '2QoRhncZ', 'fundetaxcol.turno', 'search_read', [
    [
        ['bahia_id', '=', 8842],
        ['state', 'not in', ['cancelado', 'despachado']]
    ]
], {'fields': ['id', 'name', 'state', 'sequence', 'vehiculo_id', 'conductor_id', 'bahia_id', 'anonimo']})
for t in turnos_29d:
    print(t)

# 3. fundetaxcol.turno.get_all
print("\n=== get_all PARA [8843, 8842] ===")
get_all_res = models.execute_kw(db, uid, '2QoRhncZ', 'fundetaxcol.turno', 'get_all', [], {'bahia_ids': [8843, 8842]})
print(f"Total devueltos por get_all: {len(get_all_res)}")
if get_all_res:
    print("Muestra primer turno get_all:", get_all_res[0])
