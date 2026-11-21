import re

filepath = r"C:\proxyServer\src\routes.py"
with open(filepath, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Agregar add_url_rule para print_raw
rule_target = "self.app.add_url_rule('/print/img', 'print_img', self.print_img, methods=['POST', 'OPTIONS'])"
rule_replacement = """self.app.add_url_rule('/print/img', 'print_img', self.print_img, methods=['POST', 'OPTIONS'])
        self.app.add_url_rule('/hw_proxy/print_raw', 'print_raw', self.print_raw, methods=['POST', 'OPTIONS'])"""

if "/hw_proxy/print_raw" not in code:
    code = code.replace(rule_target, rule_replacement)

# 2. Agregar el método print_raw
method_target = "    def print_img(self):"
method_code = '''    def print_raw(self):
        """Impresión directa RAW para Synergia Móvil y POS (sin pasar por HTML ni Ghostscript)."""
        try:
            if request.method == 'OPTIONS':
                resp = jsonify({'status': 'ok'})
                resp.headers.add('Access-Control-Allow-Origin', '*')
                resp.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
                resp.headers.add('Access-Control-Allow-Headers', 'Content-Type')
                return resp

            if request.is_json:
                data = request.get_json()
            else:
                data = json.loads(request.get_data().decode("utf-8"))

            params = data.get('params', data)
            raw_b64 = params.get('raw_base64') or params.get('bytes_base64') or params.get('raw')
            printer_name = params.get('printer') or ''

            actual_printer = self.printer_driver.get_printer_name(printer_name)
            if not actual_printer:
                return jsonify({"error": "No printer available"}), 400

            if not raw_b64:
                return jsonify({"error": "No raw data provided"}), 400

            raw_bytes = base64.b64decode(raw_b64) if isinstance(raw_b64, str) else raw_b64

            hPrinter = win32print.OpenPrinter(actual_printer)
            try:
                win32print.StartDocPrinter(hPrinter, 1, ("Ticket Synergia RAW", None, "RAW"))
                win32print.StartPagePrinter(hPrinter)
                win32print.WritePrinter(hPrinter, raw_bytes)
                win32print.EndPagePrinter(hPrinter)
                win32print.EndDocPrinter(hPrinter)
            finally:
                win32print.ClosePrinter(hPrinter)

            _logger.info(f"print_raw: {len(raw_bytes)} bytes ESC/POS inyectados exitosamente a {actual_printer}")
            response = jsonify({"result": True})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except Exception as e:
            _logger.error(f"Error in print_raw: {e}", exc_info=True)
            response = jsonify({"error": str(e)})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 500

    def print_img(self):'''

if "def print_raw(self):" not in code:
    code = code.replace(method_target, method_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(code)

print("C:\\proxyServer\\src\\routes.py actualizado exitosamente con print_raw!")
