import xmlrpc.client

url = 'http://fundetaxcol.co'
db = 'fundetaxcol'
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, 'admin', 'admin', {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

try:
    fields = models.execute_kw(db, uid, 'admin', 'fundetaxcol.pago', 'fields_get', [], {'attributes': ['string', 'type']})
    print("CAMPOS EN fundetaxcol.pago:", sorted(list(fields.keys())))
    
    # Probar search_read con bahia_id=8819
    res = models.execute_kw(db, uid, 'admin', 'fundetaxcol.pago', 'search_read', [
        [['bahia_id', '=', 8819]]
    ], {'fields': ['id', 'consecutivo', 'valor', 'fecha', 'vehiculo_id', 'conductor_id'], 'limit': 10})
    print("\nPAGOS ENCONTRADOS BAHIA 8819:", len(res))
    for r in res:
        print(r)
except Exception as e:
    print("ERROR:", e)
