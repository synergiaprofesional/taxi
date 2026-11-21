# Design: Real-Time Sync & Bluetooth SPP Hardening (v2.1.25+27)

## 1. Arquitectura de Real-Time y Prevención de Pérdida de Eventos

### Problema Anterior
```
server_rt_odoo -> Socket.IO -> SocketService.lastEventName.value = 'turn'
[10 segundos después]
server_rt_odoo -> Socket.IO -> SocketService.lastEventName.value = 'turn' (NO CAMBIA)
                                      |
                                      x ever() en TurnoController NO SE DISPARA
```

### Solución Diseñada
1. En `SocketService`:
   - Se mantiene `lastEventName` por compatibilidad.
   - Se introduce un `eventSequence = 0.obs` que se incrementa en CADA evento recibido, garantizando mutación de estado reactivo siempre.
   - Se expone un callback `onEventReceived(String name, dynamic data)` y método `reconnect()`.
2. En `TurnoController`:
   - Se escucha `socketService.eventSequence` con un debounce de 400ms (`debounce(socketService.eventSequence, (_) => _procesarEventoRealtime(), time: const Duration(milliseconds: 400))`).
   - Se refrescan los turnos o pagos de manera silenciosa (`cargarTurnosDesdeServidor()` / `cargarPagosDesdeServidor()`).
3. En `BahiaSelectedView`:
   - En el `AppBar`, junto al selector de Bahía, se ubica un `Obx`:
     ```dart
     Obx(() {
       final isOnline = controller.socketService.isConnected.value; // REGLA GETX: primera línea
       return GestureDetector(
         onTap: isOnline ? null : () => controller.socketService.reconnect(),
         child: Container(... badge verde si isOnline, badge ámbar "Sin RT" si !isOnline ...)
       );
     })
     ```

## 2. Arquitectura de Impresión Bluetooth SPP Nativa en Android

### Problema Anterior
`PrinterService` en Flutter llamaba a un stub `return true;`. En Android, `MainActivity.kt` no implementaba ningún canal. No se podían usar impresoras térmicas Bluetooth de cinturón.

### Solución Diseñada
1. **Canal:** `com.synergia.synergia_movil/bluetooth_printer`.
2. **Métodos:**
   - `printBytes(macAddress: String, bytes: ByteArray): Boolean`
   - `checkPermissions(): Boolean`
   - `getPairedDevices(): List<Map<String, String>>`
3. **Manejo de Conexión en `MainActivity.kt`:**
   - Para no congelar la UI de Flutter, la conexión RFCOMM se ejecuta en un thread pool (`Executors.newSingleThreadExecutor()`).
   - Socket: `device.createRfcommSocketToServiceRecord(SPP_UUID)` con fallback a `createInsecureRfcommSocketToServiceRecord(SPP_UUID)`.
   - Timeout de conexión mediante `Future` con timeout de 3500ms.
   - Escritura de bytes ESC/POS: `outStream.write(bytes)`, `outStream.flush()`, delay de 150ms para drenado térmico, y cierre seguro en `finally`.
   - Respuesta segura en `runOnUiThread` con `result.success(true)` o `result.error(...)`.
4. En `PrinterService`:
   - Invoca el canal nativo con timeout de 5 segundos. Si falla o no está en Android, retorna false y permite el fallback de previsualización sin colapsar.

