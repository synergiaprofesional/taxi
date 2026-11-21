import urllib.request
import json

def test_call():
    # 1. Authenticate
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
        print("Auth uid:", auth_res.get('result', {}).get('uid'))

    # 2. Call kw get_all
    call_url = "http://fundetaxcol.co/web/dataset/call_kw"
    call_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "fundetaxcol.turno",
            "method": "get_all",
            "args": [],
            "kwargs": {
                "bahia_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            }
        }
    }
    req2 = urllib.request.Request(
        call_url,
        data=json.dumps(call_payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Cookie': cookie
        }
    )
    try:
        with urllib.request.urlopen(req2, timeout=10) as resp2:
            res = json.loads(resp2.read().decode('utf-8'))
            print("get_all result type:", type(res.get('result')))
            if res.get('result'):
                turnos = res.get('result')
                print(f"Total turnos: {len(turnos)}")
                for t in turnos[:5]:
                    print("Turno item:", json.dumps(t, indent=2))
            else:
                print("Error or empty:", res.get('error'))
    except Exception as e:
        print("Call failed:", e)

    # 3. Also search_read
    sr_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "fundetaxcol.turno",
            "method": "search_read",
            "args": [[['state', 'in', ['espera', 'actual', 'siguiente', 'llamado']]]],
            "kwargs": {
                "fields": ['id', 'name', 'sequence', 'state', 'fecha', 'vehiculo_id', 'conductor_id', 'bahia_id', 'tarifa_id', 'total', 'anonimo', 'placa_anonima'],
                "limit": 5
            }
        }
    }
    req3 = urllib.request.Request(
        call_url,
        data=json.dumps(sr_payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Cookie': cookie
        }
    )
    try:
        with urllib.request.urlopen(req3, timeout=10) as resp3:
            res3 = json.loads(resp3.read().decode('utf-8'))
            sr_turnos = res3.get('result', [])
            print(f"search_read active turnos: {len(sr_turnos)}")
            for t in sr_turnos:
                print("search_read Turno:", json.dumps(t, indent=2))
    except Exception as e:
        print("Search read failed:", e)

if __name__ == '__main__':
    test_call()
