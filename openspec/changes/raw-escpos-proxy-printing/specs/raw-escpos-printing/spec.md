# Specification: Impresión Directa RAW ESC/POS

## Capability: RAW ESC/POS Receipt Printing via Proxy

### Scenario 1: Recepción de bytes Base64 válidos en /hw_proxy/print_raw
- **GIVEN** que el servicio `C:\proxyServer` está activo en el puerto 4000
- **AND** que la impresora `TIQUETES` está configurada en Windows
- **WHEN** un cliente HTTP envía una petición POST a `/hw_proxy/print_raw` con `bytes_base64`
- **THEN** el servicio decodifica los bytes binarios
- **AND** envía los bytes sin modificar al Spooler Win32 en modo RAW
- **AND** responde con código HTTP 200 y JSON `{"result": true}`.

### Scenario 2: Error si la impresora no está disponible
- **GIVEN** que la impresora especificada no existe en el sistema
- **WHEN** se envía una petición a `/hw_proxy/print_raw`
- **THEN** el servicio captura la excepción
- **AND** responde con código HTTP 500 y detalle del error en JSON.

### Scenario 3: Envío desde Synergia Móvil vía URL
- **GIVEN** que la app móvil tiene configurado el tipo `TipoImpresora.url` con `http://192.168.6.227:4000`
- **WHEN** el usuario pulsa Imprimir en un despacho o recibo
- **THEN** `PrinterService` genera los bytes ESC/POS y los codifica en Base64
- **AND** realiza un POST HTTP hacia `/hw_proxy/print_raw`
- **AND** el recibo físico se imprime de inmediato sin pasar por Ghostscript.
