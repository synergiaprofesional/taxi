import requests
import json
import time

url = "http://fundetaxcol.co/web/session/authenticate"
headers = {"Content-Type": "application/json"}

# 1. Login
data_login = {
    "jsonrpc": "2.0",
    "params": {
        "db": "fundetaxcol",
        "login": "admin",
        "password": "123"
    }
}
s = requests.Session()
r = s.post(url, json=data_login, headers=headers)
print("Login status:", r.status_code)
cookies = r.cookies

# 2. Test name_search for vehiculo with different queries
dataset_url = "http://fundetaxcol.co/web/dataset/call_kw"

test_queries = ['W', 'WG', 'WGM', 'WGM7', 'WGM77', 'WGM776', '']

for q in test_queries:
    t0 = time.time()
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
    r = s.post(dataset_url, json=payload, headers=headers)
    elapsed = time.time() - t0
    res = r.json()
    result = res.get('result', [])
    error = res.get('error')
    print(f"Query '{q}': {elapsed:.4f}s | Result count: {len(result)} | Items: {result[:3]} | Error: {error}")
