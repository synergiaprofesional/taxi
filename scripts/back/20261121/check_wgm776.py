import xmlrpc.client

url = 'http://fundetaxcol.co'
db = 'fundetaxcol'
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, 'admin', 'admin', {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

try:
    cars = models.execute_kw(db, uid, 'admin', 'fundetaxcol.vehiculo', 'search_read', [
        [['name', '=', 'WGM776']]
    ], {'fields': ['id', 'name', 'conductor_ids', 'numero_interno']})
    print("Vehiculo WGM776:", cars)
    if cars and cars[0].get('conductor_ids'):
        d_ids = cars[0]['conductor_ids']
        print("Conductor IDs:", d_ids)
        drivers = models.execute_kw(db, uid, 'admin', 'res.partner', 'search_read', [
            [['id', 'in', d_ids]]
        ], {'fields': ['id', 'name', 'vat', 'phone', 'mobile']})
        print("Conductores res.partner:", drivers)
except Exception as e:
    print("ERROR:", e)
