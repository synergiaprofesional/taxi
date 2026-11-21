# Especificación Normativa: Calibración Canónica de Horas y Fecha de Despacho

## Escenario 1: Parseo de hora local pre-convertida desde Odoo
- **GIVEN** que Odoo 11 retorna un timestamp pre-convertido a COT `"2026-11-02 10:11:58"` en el campo `fecha` o `create_date`
- **WHEN** la aplicación ejecuta `parseDate("2026-11-02 10:11:58")`
- **THEN** el objeto `DateTime` resultante conserva la hora `10:11`
- **AND** al formatearlo con `DateFormat('hh:mm a')` se visualiza `"10:11 AM"`, coincidiendo con el reloj del dispositivo.

## Escenario 2: Turno despachado con fecha de despacho
- **GIVEN** un registro JSON de turno con `"state": "despachado"` y `"fecha_despacho": "2026-11-02 10:20:15"`
- **WHEN** `TurnoModel.fromJson(json)` deserializa el payload
- **THEN** `turno.fechaDespacho` es un objeto `DateTime` con valor `2026-11-02 10:20:15`
- **AND** `DespachoCardWidget` visualiza `"10:20 AM"` en la cabecera del despacho en vez de la hora de llegada a la cola.

## Escenario 3: Turno en espera o sin fecha de despacho
- **GIVEN** un turno en cola con `"fecha_despacho": false` o `null`
- **WHEN** `TurnoModel.fromJson(json)` deserializa el payload
- **THEN** `turno.fechaDespacho` es `null`
- **AND** `DespachoCardWidget` (en caso de renderizarse) hace fallback seguro a `turno.fechaCreacion`.

## Escenario 4: Pagos con fecha de recaudo
- **GIVEN** un registro JSON de pago con `"fecha": "2026-11-02 10:15:30"`
- **WHEN** `PaymentModel.fromJson(json)` deserializa el pago
- **THEN** `pago.fecha` mantiene las `10:15`
- **AND** `PagoCardWidget` muestra `"10:15 AM"` en la Fila 1 de la tarjeta.

