# Change Proposal: Inyección Directa RAW ESC/POS en Hardware Proxy y App Móvil

## 1. Contexto y Justificación
Actualmente, `C:\proxyServer` (Hardware Proxy en Windows puerto 4000) procesa los recibos a través de `print_xml_receipt` convirtiendo HTML a PDF mediante `wkhtmltopdf.exe` y luego rasterizando con `Ghostscript` hacia la impresora térmica `TIQUETES`.
Este proceso introduce:
- Latencia de 2 a 4 segundos por conversión y rasterización.
- Deformación de fuentes bitmap térmicas nativas.
- Cortes de palabras antiestéticos.

El usuario solicita activar la impresión directa tal y como se hace en Windows localmente, inyectando los bytes nativos ESC/POS directamente al spooler Win32 a través del Hardware Proxy.

## 2. Capacidades Agregadas y Modificadas
- **Hardware Proxy (`C:\proxyServer`):**
  - Endpoint `POST /hw_proxy/print_raw` que recibe bytes ESC/POS en Base64 e inyecta directamente al spooler de Windows usando `win32print` con `datatype="RAW"`.
  - Soporte de fallback en `POST /hw_proxy/print_xml_receipt` si recibe el campo `bytes_base64`.
- **Synergia Móvil (`PrinterService`):**
  - Envío preferente de `bytes_base64` directamente al endpoint `/hw_proxy/print_raw` de `C:\proxyServer` en puerto 4000.
  - Tiempos de impresión reducidos de 3000 ms a < 100 ms con calidad tipográfica nativa.

## 3. Impacto y Alcance
- Afecta a `C:\proxyServer\src\routes.py`, `lib/services/printer_service.dart`, `pubspec.yaml`.
- Sin impacto negativo en Odoo POS tradicional (se mantiene compatibilidad 100% con HTML/XML existente).
