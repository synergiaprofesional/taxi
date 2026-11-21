import urllib.request
import json
import time

def test_name_search():
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
        print("Auth UID:", auth_res.get('result', {}).get('uid'))
        print("Cookie:", cookie[:50] if cookie else "None")

    headers = {
        'Content-Type': 'application/json',
        'Cookie': cookie
    }
    call_url = "http://fundetaxcol.co/web/dataset/call_kw"
    
    for q in ['W', 'WG', 'WGM', 'WGM7', 'WGM77', 'WGM776']:
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": "fundetaxcol.vehiculo",
                "method": "name_search",
                "args": [],
                "kwargs": {
                    "name": q,
                    "args": [],
                    "operator": "ilike",
                    "limit": 7
                }
            }
        }
        t0 = time.time()
        req = urllib.request.Request(
            call_url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            elapsed = time.time() - t0
            res = data.get('result')
            err = data.get('error')
            print(f"Query '{q}': {elapsed*1000:.1f}ms | Results: {res} | Error: {err}")

if __name__ == '__main__':
    test_name_search()
