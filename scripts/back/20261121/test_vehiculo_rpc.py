import json
import urllib.request

url = "http://fundetaxcol.co:8069/web/session/authenticate"
payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "db": "fundetaxcol",
        "login": "29d@fundetaxcol.co",
        "password": "123"
    }
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req) as resp:
    cookies = resp.headers.get("Set-Cookie", "")
    res = json.loads(resp.read().decode('utf-8'))
    print("Auth uid:", res.get("result", {}).get("uid"))

cookie_header = cookies.split(";")[0]

# Probar get_all en fundetaxcol.vehiculo
call_url = "http://fundetaxcol.co:8069/web/dataset/call_kw"
payload_cars = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "fundetaxcol.vehiculo",
        "method": "get_all",
        "args": [],
        "kwargs": {}
    }
}
req2 = urllib.request.Request(call_url, data=json.dumps(payload_cars).encode('utf-8'), headers={"Content-Type": "application/json", "Cookie": cookie_header})
try:
    with urllib.request.urlopen(req2) as resp2:
        cars = json.loads(resp2.read().decode('utf-8')).get("result", [])
        print(f"get_all returned {len(cars)} vehicles!")
        for c in cars:
            if "WGM776" in str(c.get("name", "")):
                print("Found WGM776 in get_all:", json.dumps(c, indent=2))
                break
except Exception as e:
    print("get_all failed:", e)

# Probar search_read en fundetaxcol.vehiculo para WGM776
payload_sr = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "fundetaxcol.vehiculo",
        "method": "search_read",
        "args": [[["name", "=", "WGM776"]]],
        "kwargs": {
            "fields": ["id", "name", "conductor_ids", "conductor_id", "numero_interno"]
        }
    }
}
req3 = urllib.request.Request(call_url, data=json.dumps(payload_sr).encode('utf-8'), headers={"Content-Type": "application/json", "Cookie": cookie_header})
try:
    with urllib.request.urlopen(req3) as resp3:
        sr_res = json.loads(resp3.read().decode('utf-8')).get("result", [])
        print("search_read WGM776:", json.dumps(sr_res, indent=2))
except Exception as e:
    print("search_read failed:", e)
