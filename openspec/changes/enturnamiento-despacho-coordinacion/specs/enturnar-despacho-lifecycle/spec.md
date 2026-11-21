# Especificación: Ciclo de Vida de Enturnamiento y Despacho

## Requerimiento Normativo
Al enturnar un vehículo, este debe ingresar a la cola de turnos con estado `espera` (o `actual` si la bahía está vacía) y permanecer en la vista de la coordinadora hasta que se ejecute la acción explícita de despacho.

### Escenario 1: Enturnar vehículo registrado en Odoo
- **GIVEN** un vehículo con placa `'WGM405'` existente en Odoo.
- **WHEN** la coordinadora presiona "Enturnar Vehículo".
- **THEN** la app debe invocar `fundetaxcol.turno.actualizar` con `anonimo: false`, `vehiculo_id: 4454`, `tarifa_id: false` y `bahia_id: 8843`.
- **AND** Odoo debe crear el turno con `state: 'espera'`.
- **AND** el turno debe aparecer de inmediato en la tarjeta de turnos en espera de la bahía.

### Escenario 2: Despacho explícito
- **GIVEN** un turno en cola con estado `espera` o `actual`.
- **WHEN** la coordinadora presiona "Despachar".
- **THEN** la app debe invocar `fundetaxcol.turno.actualizar` enviando `id: turnoId`, `state: 'despachado'`.
- **AND** el turno debe salir de la cola de turnos activos y agregarse al historial de despachos.
