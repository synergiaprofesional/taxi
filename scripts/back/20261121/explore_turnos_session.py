import urllib.request
import json

def explore_turnos_session():
    # 1. Autenticar
    auth_url = "http://fundetaxcol.co/web/session/authenticate"
    auth_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "db": "fundetaxcol",
            "login": "admin",
            "password": "admin"
        }
    }
    req = urllib.request.Request(
        auth_url,
        data=json.dumps(auth_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        cookie = resp.headers.get('Set-Cookie')
        auth_res = json.loads(resp.read().decode('utf-8'))
        uid = auth_res.get('result', {}).get('uid')
        print(f"[*] Autenticado con UID: {uid}")

    call_url = "http://fundetaxcol.co/web/dataset/call_kw"

    # 2. Consultar settings.mobile de la sesión activa
    settings_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "fundetaxcol.settings.mobile",
            "method": "get_data",
            "args": [],
            "kwargs": {"uid": uid}
        }
    }
    req2 = urllib.request.Request(
        call_url,
        data=json.dumps(settings_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Cookie': cookie}
    )
    with urllib.request.urlopen(req2, timeout=10) as resp2:
        res2 = json.loads(resp2.read().decode('utf-8'))
        settings_data = res2.get('result', {})
        current_session = settings_data.get('current_session')
        current_bay = settings_data.get('current_bay')
        print(f"[*] Settings Mobile: current_session={current_session}, current_bay={current_bay}")

    # 3. Consultar las bahías de la sesión activa
    bays_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "fundetaxcol.sesion.bahia",
            "method": "search_read",
            "args": [[['sesion_id', '=', current_session]]],
            "kwargs": {
                "fields": ['id', 'name_sec', 'name', 'state', 'turno_actual_id', 'bahia_id'],
            }
        }
    }
    req3 = urllib.request.Request(
        call_url,
        data=json.dumps(bays_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Cookie': cookie}
    )
    with urllib.request.urlopen(req3, timeout=10) as resp3:
        res3 = json.loads(resp3.read().decode('utf-8'))
        bays = res3.get('result', [])
        print(f"[*] Bahías de la sesión {current_session}:")
        bay_ids = []
        for b in bays:
            print(f"    - ID: {b.get('id')} | name_sec: '{b.get('name_sec')}' | state: '{b.get('state')}'")
            bay_ids.append(b.get('id'))

    # 4. Probar fundetaxcol.turno.get_all para las bahías activas
    target_bay = current_bay if current_bay in bay_ids else (bay_ids[0] if bay_ids else 8815)
    print(f"\n[*] Consultando get_all para bahia_id={target_bay}...")

    turnos_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "fundetaxcol.turno",
            "method": "get_all",
            "args": [],
            "kwargs": {
                "bahia_ids": [target_bay]
            }
        }
    }
    req4 = urllib.request.Request(
        call_url,
        data=json.dumps(turnos_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Cookie': cookie}
    )
    with urllib.request.urlopen(req4, timeout=10) as resp4:
        res4 = json.loads(resp4.read().decode('utf-8'))
        turnos = res4.get('result', [])
        print(f"[*] Total turnos devueltos por get_all: {len(turnos)}")

        # Clasificación
        espera = []
        despachados = []
        cancelados = []
        otros = []

        for t in turnos:
            st = t.get('state')
            tarifa = t.get('tarifa_id')
            # En Odoo tarifa_id es un Many2one o false o dict
            has_tarifa = False
            if isinstance(tarifa, list) and len(tarifa) >= 1 and tarifa[0] != 0:
                has_tarifa = True
            elif isinstance(tarifa, dict) and tarifa.get('id', 0) != 0:
                has_tarifa = True
            elif isinstance(tarifa, int) and tarifa != 0:
                has_tarifa = True

            if st == 'cancelado':
                cancelados.append(t)
            elif has_tarifa or st == 'despachado':
                despachados.append(t)
            elif st in ['espera', 'actual', 'siguiente']:
                espera.append(t)
            else:
                otros.append(t)

        print(f"[*] Desglose:")
        print(f"    - En Espera / Fila Activa: {len(espera)}")
        print(f"    - Despachados con Tarifa: {len(despachados)}")
        print(f"    - Cancelados: {len(cancelados)}")
        print(f"    - Otros: {len(otros)}")

        print("\n[*] Muestra de los primeros 5 turnos devueltos:")
        for t in turnos[:5]:
            print(f"    Seq: {t.get('sequence')} | Name: {t.get('name')} | State: {t.get('state')} | Tarifa: {t.get('tarifa_id')}")

        if espera:
            print("\n[*] Muestra de los vehículos realmente en ESPERA:")
            for t in espera[:5]:
                print(f"    Seq: {t.get('sequence')} | Name: {t.get('name')} | State: {t.get('state')} | Tarifa: {t.get('tarifa_id')}")
        else:
            print("\n[*] No hay vehículos en espera activa en esta bahía.")

if __name__ == '__main__':
    explore_turnos_session()
