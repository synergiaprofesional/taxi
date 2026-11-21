import urllib.request
import json

html = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {
      font-family: monospace;
      font-size: 13px;
      font-weight: bold;
      width: 100%;
      margin: 0;
      padding: 0;
    }
  </style>
</head>
<body>
  <div style="text-align: center;">
    <h2>TEST ZOOM PROXY</h2>
    <p>Texto al ancho completo 80mm</p>
  </div>
</body>
</html>'''

payload = {
    'params': {
        'receipt': {
            'html': html,
            'impresora': {
                'zoom': 1.35,
                'page_width': 80,
                'mt': 0,
                'mb': 0,
                'mr': 0,
                'ml': 0
            }
        }
    }
}

req = urllib.request.Request(
    'http://127.0.0.1:4000/hw_proxy/print_xml_receipt',
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
resp = urllib.request.urlopen(req)
print("Respuesta:", resp.read().decode())
