import urllib.request
import json

url = "http://127.0.0.1:4000/hw_proxy/print_xml_receipt"
html_content = """
<html>
<body style="font-family: monospace; font-size: 12px; margin: 0; padding: 5px;">
    <div style="text-align: center;">
        <h3>FUNDETAXCOL / SYNERGIA MOVIL</h3>
        <p>NIT 900.542.188-4<br>BAHIA: Garita</p>
        <hr>
        <h2>TURNO #108</h2>
        <p><b>RAMON DE JESUS QUINTANA TEJEDOR</b></p>
        <hr>
    </div>
    <p>PLACA: TF0008<br>
    CONDUCTOR: RAMON DE JESUS QUINTANA TEJEDOR<br>
    DESTINO: MANGA / PPAL<br>
    DIRECCION: Calle 30 # 20-15<br>
    FECHA: 18/10/2026 18:50:00<br>
    OPERADOR: 29d@fundetaxcol.co</p>
    <hr>
    <h3>TOTAL: $ 12.000</h3>
</body>
</html>
"""

payload = {
    "params": {
        "receipt": html_content
    }
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req, timeout=5) as response:
        print("Status code:", response.status)
        print("Response:", response.read().decode())
except Exception as e:
    print("Error:", e)
