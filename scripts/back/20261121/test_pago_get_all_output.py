import urllib.request
import json

url = "http://fundetaxcol.co/web/dataset/call_kw"

# Login first
auth_data = {
    "jsonrpc": "2.0",
    "params": {
        "db": "fundetaxcol",
        "login": "garita",
        "password": "123"
    }
}
req = urllib.request.Request(
    "http://fundetaxcol.co/web/session/authenticate",
    data=json.dumps(auth_data).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)
res = urllib.request.urlopen(req)
cookie = res.headers.get("Set-Cookie")
auth_res = json.loads(res.read().decode())
print("Auth UID:", auth_res.get("result", {}).get("uid"))

# Call fundetaxcol.pago.get_all
payload = {
    "jsonrpc": "2.0",
    "params": {
        "model": "fundetaxcol.pago",
        "method": "get_all",
        "args": [],
        "kwargs": {
            "bahia_ids": [8838, 8839, 8840]
        }
    }
}
req2 = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json", "Cookie": cookie}
)
res2 = urllib.request.urlopen(req2)
data2 = json.loads(res2.read().decode())
results = data2.get("result", [])
print(f"Total pagos devueltos por get_all: {len(results)}")
if results:
    first = results[0]
    print("\nPrimer pago:")
    print("id:", first.get("id"), type(first.get("id")))
    print("consecutivo:", first.get("consecutivo"))
    print("bahia_id:", first.get("bahia_id"), type(first.get("bahia_id")))
    print("vehiculo_id:", first.get("vehiculo_id"), type(first.get("vehiculo_id")))
    print("conductor_id:", first.get("conductor_id"), type(first.get("conductor_id")))
    print("total:", first.get("total"), type(first.get("total")))
    print("valor:", first.get("valor"), type(first.get("valor")))
    print("fecha:", first.get("fecha"), type(first.get("fecha")))
