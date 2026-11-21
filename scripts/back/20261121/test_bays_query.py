import urllib.request
import json

def test_bays():
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
        uid = auth_res.get('result', {}).get('uid')
        print(f"Auth uid: {uid}")

    call_url = "http://fundetaxcol.co/web/dataset/call_kw"

    # 2. Call fundetaxcol.settings.mobile get_data
    settings_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "fundetaxcol.settings.mobile",
            "method": "get_data",
            "args": [],
            "kwargs": {
                "uid": uid
            }
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
        print("Settings Mobile Data:", json.dumps(settings_data, indent=2))
        curr_session = settings_data.get('current_session')

    # 3. Call fundetaxcol.sesion.bahia with current_session and name_sec
    bays_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "fundetaxcol.sesion.bahia",
            "method": "search_read",
            "args": [[['sesion_id', '=', curr_session]]],
            "kwargs": {
                "fields": ['id', 'name_sec', 'name', 'state', 'bahia_id'],
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
        print(f"Bays for session {curr_session} (Total: {len(bays)}):")
        for b in bays:
            print(f"  ID: {b.get('id')} | name_sec: '{b.get('name_sec')}' | name: '{b.get('name')}'")

if __name__ == '__main__':
    test_bays()
