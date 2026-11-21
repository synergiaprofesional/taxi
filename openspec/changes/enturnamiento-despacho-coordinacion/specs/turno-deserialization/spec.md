# Especificación: Deserialización Polimórfica de Turnos

## Requerimiento Normativo
`TurnoModel.fromJson` debe deserializar sin pérdida de información los identificadores de relación Many2one provenientes de Odoo 11 tanto si vienen formateados como `Map` (`_get_data`), `List` (`search_read`) o `int`.

### Escenario 1: Deserialización de bahia_id como Map
- **GIVEN** una respuesta RPC de Odoo donde `'bahia_id'` es `{'id': 8843, 'name': 'Garita Sesión [2026-10-25]'}`.
- **WHEN** se ejecuta `TurnoModel.fromJson(json)`.
- **THEN** `bahiaSesionId` debe ser exactamente `8843` y `bahiaNombre` debe ser `'Garita Sesión [2026-10-25]'`.

### Escenario 2: Deserialización de bahia_id como List
- **GIVEN** una respuesta RPC donde `'bahia_id'` es `[8843, 'Garita Sesión [2026-10-25]']`.
- **WHEN** se ejecuta `TurnoModel.fromJson(json)`.
- **THEN** `bahiaSesionId` debe ser exactamente `8843` y `bahiaNombre` debe ser `'Garita Sesión [2026-10-25]'`.

### Escenario 3: Filtro por bahía activa
- **GIVEN** un `TurnoModel` con `bahiaSesionId == 8843`.
- **WHEN** `bahiaIdActual.value == 8843`.
- **THEN** el turno debe incluirse en la lista observable `turnosEnFila` si su estado es `espera` o `actual`.
