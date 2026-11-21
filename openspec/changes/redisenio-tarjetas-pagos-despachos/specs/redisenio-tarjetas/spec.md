# Especificación: Desacoplamiento Estricto de Tarjetas (Turnos vs Despachos vs Pagos)

## Capability: Desacoplamiento de Widgets de Tarjeta

### Scenario: Renderizado de Tarjeta de Turno en Cola (Original Intacto)
- **GIVEN** un turno en fila de espera `TurnoModel` en `TurnoListView`.
- **WHEN** se construye el widget `TurnoCardWidget`.
- **THEN** debe renderizar el avatar con el número de turno.
- **AND** en la columna central debe mostrar la placa visible en la línea 1 y el conductor con el tiempo de espera en la línea 2.
- **AND** en la columna trailing derecha debe mostrar la hora en la parte superior y el badge de estado (`ACTUAL` o nombre de bahía) en la parte inferior.
- **AND** NO debe renderizar ninguna tercera fila ni precio de despacho.

### Scenario: Renderizado de Tarjeta de Despacho (Componente Dedicado)
- **GIVEN** un turno despachado `TurnoModel` en `DespachoListView` o `DespachoHistoryView`.
- **WHEN** se construye el widget dedicado `DespachoCardWidget`.
- **THEN** la Fila 1 debe mostrar horizontalmente `Placa`, `Turno`, la hora del despacho y `$Valor` al extremo derecho.
- **AND** la Fila 2 debe mostrar el nombre del conductor.
- **AND** la Fila 3 debe mostrar el destino oficial y la dirección o nota complementaria si existe.

### Scenario: Renderizado de Tarjeta de Pago
- **GIVEN** un modelo de recaudo `PagoRecaudoModel` en `PagoListView`.
- **WHEN** se construye el widget `PagoCardWidget`.
- **THEN** la Fila 1 muestra `Placa`, `Tiquete`, hora y `$Total`.
- **AND** la Fila 2 muestra el conductor.
- **AND** la Fila 3 muestra el nombre de la bahía.
