import requests

url = 'https://helados.synergiapos.co'
print(f"Probando {url}...")
try:
    r = requests.get(url, timeout=12, allow_redirects=True)
    print(f"URL Final: {r.url}")
    print(f"Status Code: {r.status_code}")
    print(f"Server: {r.headers.get('Server')}")
    titles = [line.strip() for line in r.text.splitlines() if '<title>' in line.lower()]
    print(f"Title: {titles}")
    print(f"Bytes: {len(r.text)}")
    print("Contenido inicial:")
    print(r.text[:300])
except Exception as e:
    print(f"Error al conectar: {e}")
