# Spec: Sincronización en Tiempo Real e Impresión Bluetooth SPP

## 1. Notificaciones en Tiempo Real (Socket.IO)

### Escenario 1: Recepción de eventos repetidos consecutivos
- **GIVEN** el despachador está en la vista de Bahía con turnos activos
- **WHEN** el servidor emite dos eventos consecutivos con el mismo nombre (ej. `'turn'` y `'turn'`)
- **THEN** `SocketService.eventSequence` debe incrementarse en ambos casos
- **AND** `TurnoController` debe refrescar la lista de turnos mediante la llamada al servidor sin omitir el segundo evento.

### Escenario 2: Indicador visual de estado de tiempo real
- **GIVEN** la vista `BahiaSelectedView` está desplegada
- **WHEN** `SocketService.isConnected` es `true`
- **THEN** el `AppBar` debe mostrar un indicador verde con tooltip "Tiempo real activo"
- **WHEN** `SocketService.isConnected` pasa a `false`
- **THEN** el `AppBar` debe mostrar un indicador de advertencia ("Sin RT") y permitir hacer tap para ejecutar `reconnect()`.

## 2. Impresión Bluetooth SPP

### Escenario 1: Envío de tiquete a impresora térmica Bluetooth en Android
- **GIVEN** el usuario tiene configurada una impresora tipo Bluetooth con su dirección MAC
- **WHEN** se genera un despacho o se solicita reimprimir tiquete
- **THEN** `PrinterService` debe invocar el canal nativo `com.synergia.synergia_movil/bluetooth_printer` con el método `printBytes`
- **AND** `MainActivity.kt` debe conectar por RFCOMM en segundo plano, inyectar los bytes ESC/POS y retornar éxito en menos de 4 segundos sin congelar la interfaz.

### Escenario 2: Impresora Bluetooth apagada o fuera de alcance
- **GIVEN** la impresora térmica está apagada o con batería agotada
- **WHEN** se solicita la impresión
- **THEN** el intento de conexión debe agotar el tiempo límite (timeout 3.5s)
- **AND** la app debe retornar error controlado sin crashear ni congelarse, abriendo el diálogo de previsualización de tiquete.

