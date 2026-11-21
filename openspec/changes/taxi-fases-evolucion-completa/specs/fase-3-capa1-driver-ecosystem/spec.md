## ADDED Requirements

### Requirement: Turno y Posición en Cola en Tiempo Real para Conductor
El sistema SHALL mostrar en el smartphone del conductor su posición exacta en la fila y la bahía activa, actualizándose instantáneamente ante cualquier cambio en el backend.

#### Scenario: Visualización de Turno
- **WHEN** un vehículo es despachado por delante en la fila
- **THEN** el número de turno del conductor en espera disminuye automáticamente sin recargar la pantalla

### Requirement: Billetera de Ahorro Programado y Liquidación
El sistema SHALL presentar el balance acumulado de ahorros del conductor y el historial de pagos de sostenimiento y planilla de viaje.

#### Scenario: Consulta de Saldo de Ahorro
- **WHEN** el conductor abre la pestaña de liquidación
- **THEN** visualiza el total ahorrado en el año en curso y el detalle de los últimos aportes validados

### Requirement: Botón de Pánico y Red de Seguridad
El sistema SHALL permitir al conductor disparar una alerta de auxilio transmitiendo sus coordenadas GPS en tiempo real a la garita y a los taxistas cercanos.

#### Scenario: Activación de Emergencia
- **WHEN** el conductor mantiene presionado el botón de auxilio por 2 segundos
- **THEN** el sistema registra el evento en Firestore y notifica de inmediato al centro de despacho con su ubicación
