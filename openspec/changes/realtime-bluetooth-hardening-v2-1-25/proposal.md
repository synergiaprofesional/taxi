# Change: Real-Time Sync & Bluetooth SPP Hardening (v2.1.25+27)

## Contexto y Motivación
En el ciclo `v2.1.24+26` se completaron las 7 novedades operativas del informe del cliente. No obstante, la auditoría técnica profunda y el blast radius revelaron 3 pendientes críticos de infraestructura:
1. **Pérdida de eventos Real-Time repetidos:** `SocketService` actualizaba `lastEventName` (`RxString`), pero cuando dos eventos del mismo nombre llegaban secuencialmente (ej. dos turnos seguidos `'turn'`), GetX no mutaba el valor y `TurnoController` no disparaba la recarga de la cola. Además, no existía feedback visual de conectividad en el `AppBar`, operando a ciegas si el socket se desconectaba.
2. **Impresión Bluetooth SPP Mockeada:** La rama `TipoImpresora.bluetooth` en `PrinterService` era un stub que retornaba `true` sin enviar bytes, y `MainActivity.kt` no implementaba el `MethodChannel`. En campo, los despachadores requieren imprimir tiquetes térmicos vía impresoras portátiles Bluetooth.
3. **Gobierno OpenSpec:** El change anterior requería archivarse formalmente y abrirse el nuevo cambio con versionamiento continuo `v2.1.25+27`.

## Alcance
- `lib/services/socket_service.dart`: desacoplamiento de eventos con contador de secuencia / stream reactivo y método `reconnect()`.
- `lib/controllers/turno_controller.dart`: debouncing de 400ms para recarga silenciosa de turnos, despachos y pagos ante ráfagas socket.
- `lib/ui/views/main/bahia_selected_view.dart`: indicador visual compacto en `AppBar` (punto verde "Tiempo real activo" o badge ámbar/rojo "Sin RT" con tap para reconectar). Cumpliendo estrictamente la regla GetX de lectura temprana de variables reactivas.
- `android/app/src/main/kotlin/com/synergia/synergia_movil/MainActivity.kt`: implementación nativa Android de `MethodChannel` (`com.synergia.synergia_movil/bluetooth_printer`) con conexión RFCOMM en hilo de fondo (`Dispatchers.IO` / `Executors`), timeout de 3.5 segundos, UUID SPP estándar `00001101-0000-1000-8000-00805F9B34FB`, y flush de buffer.
- `lib/services/printer_service.dart`: canal Bluetooth nativo conectado con timeout seguro de 5s y fallback controlado a vista previa.
- Verificación estática (`flutter analyze` -> 0 issues), suite de tests, y despliegue físico verificado en Windows y Xiaomi.

