# Especificación: Deserialización Polimórfica de Pagos

## Capability: payment-deserialization

### Scenario 1: Deserialización desde respuesta RPC de Odoo `_get_data()` (Diccionarios Map)
- **GIVEN** una respuesta JSON de Odoo donde `bahia_id` es `{'id': 1, 'name': 'Av. Lago'}`, `vehiculo_id` es `{'id': 4066, 'name': 'WGN772'}` y `conductor_id` es `{'id': 4447, 'name': 'ISIDORO DIAZ AVILA'}`.
- **WHEN** se instancia `PagoRecaudoModel.fromJson(json)`.
- **THEN** `bahiaId` debe ser `1`, `bahiaNombre` debe ser `'Av. Lago'`, `placa` debe ser `'WGN772'`, `conductorNombre` debe ser `'ISIDORO DIAZ AVILA'` y no debe lanzarse ninguna excepción de tipado.

### Scenario 2: Deserialización desde respuesta `search_read` (Listas Many2one)
- **GIVEN** una respuesta JSON donde `bahia_id` es `[8840, 'Garita Sesión [2026-10-24]']`, `vehiculo_id` es `[4066, 'WGN772']` y `conductor_id` es `[4447, 'ISIDORO DIAZ AVILA']`.
- **WHEN** se instancia `PagoRecaudoModel.fromJson(json)`.
- **THEN** los IDs y nombres correspondientes deben extraerse de los índices `0` y `1` respectivamente sin fallar.
