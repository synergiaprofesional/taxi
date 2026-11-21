# Design Document: Inyección Directa RAW ESC/POS

## 1. Arquitectura de Impresión Directa

```
┌─────────────────────────────────┐
│ Tablet / Móvil (Synergia Móvil) │
│ Genera Bytes Binarios ESC/POS   │
└────────────────┬────────────────┘
                 │ HTTP POST {"bytes_base64": "..."}
                 ▼
┌─────────────────────────────────┐
│ C:\proxyServer (Waitress :4000) │
│ Endpoint /hw_proxy/print_raw    │
└────────────────┬────────────────┘
                 │ win32print.WritePrinter(hPrinter, RAW)
                 ▼
┌─────────────────────────────────┐
│ Windows Spooler -> TIQUETES     │
│ Impresión Térmica Instantánea   │
└─────────────────────────────────┘
```

## 2. Contrato de API: `/hw_proxy/print_raw`
- **Método:** `POST`
- **Headers:** `Content-Type: application/json`
- **Body Payload:**
  ```json
  {
    "params": {
      "bytes_base64": "G0BAN0JBSElBOiBHYXJpdGEK...",
      "printer": "TIQUETES"
    }
  }
  ```
- **Respuesta:**
  ```json
  { "result": true }
  ```

## 3. Implementación en `win32print`
```python
hPrinter = win32print.OpenPrinter(printer_name)
try:
    win32print.StartDocPrinter(hPrinter, 1, ("Ticket Synergia RAW", None, "RAW"))
    win32print.StartPagePrinter(hPrinter)
    win32print.WritePrinter(hPrinter, raw_bytes)
    win32print.EndPagePrinter(hPrinter)
    win32print.EndDocPrinter(hPrinter)
finally:
    win32print.ClosePrinter(hPrinter)
```

## 4. Fallback y Resiliencia
Si el proxy no tiene la ruta `/hw_proxy/print_raw`, `PrinterService` intentará `/hw_proxy/print_xml_receipt` con el payload de compatibilidad.
