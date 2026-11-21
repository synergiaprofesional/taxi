import urllib.request
import json

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

# Search vehicles with "776"
call_url = "http://fundetaxcol.co/web/dataset/call_kw"
call_payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "fundetaxcol.vehiculo",
        "method": "search_read",
        "args": [[["name", "ilike", "776"]]],
        "kwargs": {
            "fields": ["id", "name", "conductor_ids", "numero_interno"]
        }
    }
}
req2 = urllib.request.Request(
    call_url,
    data=json.dumps(call_payload).encode('utf-8'),
    headers={'Content-Type': 'application/json', 'Cookie': cookie}
)
with urllib.request.urlopen(req2, timeout=10) as resp2:
    res = json.loads(resp2.read().decode('utf-8'))
    print("Vehiculos encontrados con '776':", json.dumps(res.get('result', []), indent=2))
