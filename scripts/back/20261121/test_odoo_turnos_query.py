import urllib.request
import json

def test_query():
    url = "http://fundetaxcol.co/web/session/authenticate"
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "db": "fundetaxcol",
            "login": "admin",
            "password": "admin"
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=6) as response:
            cookie = response.headers.get('Set-Cookie')
            res_data = json.loads(response.read().decode('utf-8'))
            print("Auth response:", res_data.get('result', {}).get('name') or res_data.get('error'))
            return cookie
    except Exception as e:
        print("Auth failed:", e)
        return None

if __name__ == '__main__':
    test_query()
